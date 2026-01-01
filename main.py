from fastapi import FastAPI
from db.db_factory import DataBaseFactory

app = FastAPI()

db = DataBaseFactory.get_client()


@app.post("/create_document")
async def create_document(text: str):
    db.insert_data(text)
    return {"message": "Document created successfully"}

@app.get("/get_documents")
async def get_documents():
    return db.get_data()
