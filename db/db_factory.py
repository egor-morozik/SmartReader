from re import match
from typing import Optional
from dotenv import load_dotenv
from .db_interface import DataBaseInterface

import os

load_dotenv()

class DataBaseFactory:
    _instance: Optional[DataBaseInterface] = None

    @classmethod
    def _create_client(cls) -> DataBaseInterface:
        db_system = os.getenv("DB_SYSTEM", "").lower()
        match db_system:
            case "supabase":
                from .db_clients.db_supabase import SupabaseDBClient
                return SupabaseDBClient()
            case _:
                raise ValueError(f"Unsupported database type: {db_system}")
            
    @classmethod
    def get_client(cls) -> DataBaseInterface:
        if cls._instance is None:
            cls._instance = cls._create_client()
        return cls._instance
    