from abc import ABC, abstractmethod

class BaseKnowledge(ABC):
    def __init__(self):
        self.data = {}

    @abstractmethod
    def add(self, key, value):
        pass

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def update(self, key, value):
        pass

    @abstractmethod
    def delete(self, key):
        pass

    @abstractmethod
    def clear(self):
        pass