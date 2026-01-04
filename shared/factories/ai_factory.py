from ..interfaces.ai_interface import AiInterface


class AiFactory:
    @classmethod
    def get_client(cls, ai_system: str = "") -> AiInterface:
        match ai_system.lower():
            case "groq":
                from ..implementations.ai_groq import GroqClient

                return GroqClient()
            case _:
                raise ValueError(f"Unsupported ai system: {ai_system}")
