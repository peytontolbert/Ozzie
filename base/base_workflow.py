from abc import ABC, abstractmethod

class BaseWorkflow(ABC):
    def __init__(self, name, steps, error_handling="continue"):
        self.name = name
        self.steps = []
        self.error_handling = error_handling
        self.estimated_runtime = 0
        self.add_steps(steps)

    def add_steps(self, steps):
        for step in steps:
            self.add_step(step)

    def add_step(self, step):
        if callable(step):
            self.steps.append(step)
        else:
            raise TypeError(f"Step must be callable, got {type(step)}")

    def get_steps(self):
        return self.steps

    def set_estimated_runtime(self, runtime):
        self.estimated_runtime = runtime

    def get_estimated_runtime(self):
        return self.estimated_runtime

    @abstractmethod
    def execute(self):
        pass

    def __str__(self):
        return f"Workflow: {self.name} with {len(self.steps)} steps"