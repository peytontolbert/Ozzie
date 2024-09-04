from base.base_workflow import BaseWorkflow
from tasks.task_queue import TaskQueue

class WorkflowEngine:
    def __init__(self):
        self.workflows = {}
        self.task_queue = TaskQueue()

    def register_workflow(self, workflow_name, workflow):
        if not isinstance(workflow, BaseWorkflow):
            raise TypeError("Workflow must be an instance of BaseWorkflow")
        self.workflows[workflow_name] = workflow

    def execute_workflow(self, workflow_name, *args, **kwargs):
        if workflow_name not in self.workflows:
            raise ValueError(f"Workflow '{workflow_name}' not found")
        
        workflow = self.workflows[workflow_name]
        for step in workflow.steps:
            self.task_queue.add_task(step, *args, **kwargs)
        
        results = []
        while not self.task_queue.is_empty():
            task, task_args, task_kwargs = self.task_queue.get_next_task()
            try:
                result = task(*task_args, **task_kwargs)
                results.append(result)
            except Exception as e:
                results.append(f"Error executing task: {str(e)}")
        
        return results

    def get_workflow(self, workflow_name):
        return self.workflows.get(workflow_name)

    def list_workflows(self):
        return list(self.workflows.keys())

    def remove_workflow(self, workflow_name):
        if workflow_name in self.workflows:
            del self.workflows[workflow_name]
            return True
        return False