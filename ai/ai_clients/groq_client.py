from ..ai_interface import AiInterface
from groq import Groq
from dotenv import load_dotenv

import os

load_dotenv()

class GroqClient(AiInterface):
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_KEY",""))
        self.defaults = {
            "model": "llama-3.3-70b-versatile",
            "temperature": 0.3,
            "max_tokens": 256,
        }

    def send(self, query: str = "") -> str:
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": query}],
            **self.defaults
        )
        return response.choices[0].message.content
