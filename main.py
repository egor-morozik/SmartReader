from fastapi import FastAPI
from db.db_factory import DataBaseFactory
from ai.ai_factory import AiFactory
from dotenv import load_dotenv

import os 

load_dotenv()

app = FastAPI()

db = DataBaseFactory.get_client()
ai = AiFactory.get_client(os.getenv("AI_SYSTEM", ""))

@app.post("/create_document")
async def create_document(text: str):
    text = ai.send(text)
    db.insert_data(text)
    return {"message": "Document created successfully",
            "new version" : text}

@app.get("/get_documents")
async def get_documents():
    return db.get_data()
