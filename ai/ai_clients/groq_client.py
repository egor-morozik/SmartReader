from ..ai_interface import AiInterface

class GroqClient(AiInterface):
    def __init__(self):
        pass

    def send(self, query: str = "") -> str:
        return query[0:100]
