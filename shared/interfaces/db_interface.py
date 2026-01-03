from abc import ABC, abstractmethod

class DataBaseInterface(ABC):
    @abstractmethod
    def insert_documents_data(self, data: str) -> str:
        pass

    @abstractmethod 
    def get_documents_data(self) -> str:
        pass

    @abstractmethod
    def insert_summary_data(self, data: str) -> str:
        pass

    @abstractmethod 
    def get_summary_data(self) -> str:
        pass
