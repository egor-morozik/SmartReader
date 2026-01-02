from ..interfaces.db_interface import DataBaseInterface
from dotenv import load_dotenv
from supabase import create_client

import os

load_dotenv()

class SupabaseDBClient(DataBaseInterface):
    def __init__(self):
        self._client = create_client(
            os.getenv("SUPABASE_URL"), 
            os.getenv("SUPABASE_KEY")
            )
        self._documents_table = os.getenv("DB_TABLE_DOCUMENTS")
        self._summaries_table = os.getenv("DB_TABLE_SUMMARIES")

    def insert_documents_data(self, data):
        response = self._client.table(self._documents_table).insert({"text": data}).execute()
        return response.data

    def get_documents_data(self):
        response = self._client.table(self._documents_table).select("*").execute()
        return response.datas

    def insert_summary_data(self, data):
        response = self._client.table(self._summaries_tabl).insert({"text": data}).execute()
        return response.data

    def get_summary_data(self):
        response = self._client.table(self._summaries_table).select("*").execute()
        return response.datas
    