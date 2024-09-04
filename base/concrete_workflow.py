from base.base_workflow import BaseWorkflow

class ConcreteWorkflow(BaseWorkflow):
    def execute(self):
        results = []
        for step in self.steps:
            try:
                result = step()
                results.append(result)
            except Exception as e:
                results.append(f"Error executing step: {str(e)}")
                if self.error_handling == "stop_on_error":
                    break
        return results