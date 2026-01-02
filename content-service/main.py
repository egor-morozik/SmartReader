import pika
import json
import os

from fastapi import FastAPI
from datetime import datetime
from dotenv import load_dotenv

from shared.factories.db_factory import DataBaseFactory

load_dotenv()

db = DataBaseFactory.get_client()

def get_rabbitmq_channel():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.getenv("RABBITMQ_HOST", "rabbitmq"),
            port=5672
        )
    )
    return connection.channel()

app = FastAPI()

@app.post("/documents")
async def create_document(document: str):
    data = {
        "text": document.text,
        "created_at": datetime.datetime().isoformat()
    }
    
    response = db.insert_data(data)
    
    document_id = response[0]["id"] if isinstance(response, list) and response else None
    
    channel = get_rabbitmq_channel()
    channel.queue_declare(queue='document_to_summarize', durable=True)
    
    message = {
        "document_id": document_id,
        "text": document.text
    }
    
    channel.basic_publish(
        exchange='',
        routing_key='document_to_summarize',
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )
    
    channel.close()
    
    return {
        "id": document_id,
        "message": "Document created and sent for summarization"
    }
        
@app.get("/documents")
async def get_all_documents():
    return db.get_data()
