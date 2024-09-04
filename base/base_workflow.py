from abc import ABC, abstractmethod

class BaseWorkflow(ABC):
    def __init__(self, name):
        self.name = name
        self.steps = []

    @abstractmethod
    def execute(self):
        pass

    def add_step(self, step):
        if callable(step):
            self.steps.append(step)
        else:
            raise TypeError("Step must be a callable")

    def remove_step(self, index):
        if 0 <= index < len(self.steps):
            return self.steps.pop(index)
        else:
            raise IndexError("Step index out of range")

    def get_steps(self):
        return self.steps

    def execute(self):
        results = []
        for step in self.steps:
            try:
                result = step()
                results.append(result)
            except Exception as e:
                results.append(f"Error executing step: {str(e)}")
        return results

    def __str__(self):
        return f"Workflow: {self.name} with {len(self.steps)} steps"