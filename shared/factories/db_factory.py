import os
from typing import Optional

from dotenv import load_dotenv

from ..interfaces.db_interface import DataBaseInterface

load_dotenv()


class DataBaseFactory:
    _instance: Optional[DataBaseInterface] = None

    @classmethod
    def _create_client(cls) -> DataBaseInterface:
        db_system = os.getenv("DB_SYSTEM", "supabase").lower()
        match db_system:
            case "supabase":
                from ..implementations.db_supabase import SupabaseDBClient

                return SupabaseDBClient()
            case _:
                raise ValueError(f"Unsupported database type: {db_system}")

    @classmethod
    def get_client(cls) -> DataBaseInterface:
        if cls._instance is None:
            cls._instance = cls._create_client()
        return cls._instance
