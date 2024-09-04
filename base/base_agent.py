from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name):
        self.name = name
        self.memory = {}
        self.skills = set()
        self.goals = []

    @abstractmethod
    def perform_action(self, action):
        pass

    @abstractmethod
    def learn(self, experience):
        pass

    @abstractmethod
    def update_goals(self, new_goals):
        pass

    def add_skill(self, skill):
        self.skills.add(skill)

    def remove_skill(self, skill):
        self.skills.discard(skill)

    def set_memory(self, key, value):
        self.memory[key] = value

    def get_memory(self, key):
        return self.memory.get(key)

    def clear_memory(self):
        self.memory.clear()