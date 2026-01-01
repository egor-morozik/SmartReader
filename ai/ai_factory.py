from re import match
from typing import Optional
from dotenv import load_dotenv
from .ai_interface import AiInterface

class AiFactory:
    @classmethod
    def get_client(cls, ai_system: str = "") -> AiInterface:
        match ai_system.lower():
            case "groq":
                from .ai_clients.groq_client import GroqClient
                return GroqClient()
            case _:
                raise ValueError(f"Unsupported ai system: {ai_system}")
            
    