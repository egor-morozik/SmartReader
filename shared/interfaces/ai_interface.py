from abc import ABC, abstractmethod


class AiInterface(ABC):
    @abstractmethod
    def send(self, query: str) -> str:
        pass
