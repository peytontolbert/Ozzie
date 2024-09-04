from base.base_workflow import BaseWorkflow

class WorkflowDesigner:
    def __init__(self):
        self.available_steps = {}

    def register_step(self, step_name, step_function):
        if not callable(step_function):
            raise TypeError("Step function must be callable")
        self.available_steps[step_name] = step_function

    def create_workflow(self, name, step_sequence):
        class CustomWorkflow(BaseWorkflow):
            def __init__(self, workflow_name, steps):
                super().__init__(workflow_name)
                self.steps = steps

            def execute(self):
                results = []
                for step in self.steps:
                    try:
                        results.append(step())
                    except Exception as e:
                        results.append(f"Error executing step: {str(e)}")
                return results

        workflow_steps = []
        for step_name in step_sequence:
            if step_name not in self.available_steps:
                raise ValueError(f"Step '{step_name}' not found in available steps")
            workflow_steps.append(self.available_steps[step_name])

        return CustomWorkflow(name, workflow_steps)

    def list_available_steps(self):
        return list(self.available_steps.keys())

    def get_step_details(self, step_name):
        if step_name in self.available_steps:
            return self.available_steps[step_name].__doc__
        return None