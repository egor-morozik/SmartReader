from abc import ABC, abstractmethod

class DataBaseInterface(ABC):
    @abstractmethod
    def insert_data(self, data):
        pass

    @abstractmethod 
    def get_data(self):
        pass
