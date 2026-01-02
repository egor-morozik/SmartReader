from ..interfaces.ai_interface import AiInterface
from groq import Groq
from dotenv import load_dotenv

import os

load_dotenv()

class GroqClient(AiInterface):
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_KEY",""))
        self.defaults = {
            "model": os.getenv("AI_MODEL","llama-3.3-70b-versatile"),
            "temperature": float(os.getenv("AI_TEMPERATURE", 0.3)),
            "max_tokens": int(os.getenv("AI_MAX_TOKENS", 256)),
        }

    def send(self, query: str = "") -> str:
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": query}],
            **self.defaults
        )
        return response.choices[0].message.content
