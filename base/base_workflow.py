from abc import ABC, abstractmethod

class BaseWorkflow(ABC):
    def __init__(self, name):
        self.name = name
        self.steps = []

    @abstractmethod
    def execute(self):
        pass

    def add_step(self, step):
        self.steps.append(step)

    def remove_step(self, step):
        self.steps.remove(step)

    def clear_steps(self):
        self.steps.clear()

    def get_step_count(self):
        return len(self.steps)