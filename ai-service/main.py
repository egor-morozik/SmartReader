import json
import os
import threading
import time
from contextlib import asynccontextmanager

import pika
from dotenv import load_dotenv
from fastapi import FastAPI

from shared.factories.ai_factory import AiFactory
from shared.factories.db_factory import DataBaseFactory

load_dotenv()

ai = AiFactory.get_client(os.getenv("AI_SYSTEM", "groq"))
db = DataBaseFactory.get_client()


def summarize_text(text: str) -> str:
    prompt = f"""Reduce this text to a minimum,
                conveying its general meaning. In response,
                return only the new text: {text}"""

    return ai.send(prompt)


def process_message(body: str) -> str:
    message = json.loads(body)
    document_id = message["document_id"]
    text = message["text"]

    summary_text = summarize_text(text)

    data = {"document_id": document_id, "text": summary_text}

    db.insert_summary_data(data)

    return True


def wait_for_rabbitmq() -> bool:
    for _ in range(30):
        try:
            test_connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=os.getenv("RABBITMQ_HOST", "rabbitmq"), port=5672
                )
            )
            test_connection.close()
            return True
        except BaseException:
            time.sleep(2)
    return False


def start_consumer() -> None:
    if not wait_for_rabbitmq():
        return

    while True:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=os.getenv("RABBITMQ_HOST", "rabbitmq"), port=5672
            )
        )
        channel = connection.channel()

        channel.queue_declare(queue="document_to_summarize", durable=True)
        channel.basic_qos(prefetch_count=1)

        def callback(ch, method, properties, body):
            if process_message(body):
                ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        channel.basic_consume(
            queue="document_to_summarize", on_message_callback=callback
        )

        channel.start_consuming()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global consumer_thread, stop_consumer

    stop_consumer = threading.Event()

    consumer_thread = threading.Thread(target=start_consumer, daemon=True)
    consumer_thread.start()

    yield

    stop_consumer.set()

    if consumer_thread and consumer_thread.is_alive():
        consumer_thread.join(timeout=5)


app = FastAPI(lifespan=lifespan)


@app.post("/summarize")
async def summarize_direct(text: str):
    return {
        "summary": summarize_text(text),
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "ai_system": os.getenv("AI_SYSTEM", "unknown"),
    }
