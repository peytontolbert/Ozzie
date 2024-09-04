from base.base_workflow import BaseWorkflow
from tasks.task_queue import TaskQueue
from functools import lru_cache
import json
from base.concrete_workflow import ConcreteWorkflow

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

    def generate_workflow(self, intent_str):
        # Parse the intent string
        intent = json.loads(intent_str)
        
        # Generate steps based on the intent
        steps = self._generate_steps(intent)
        
        # Create and return a new ConcreteWorkflow instance
        return ConcreteWorkflow(name=f"Workflow for {intent['action']}", steps=steps)

    def _generate_steps(self, intent):
        steps = []
        
        def create_step(message):
            return lambda: print(message)

        action_handlers = {
            'inform': self._handle_inform,
            'recommend': self._handle_recommend,
            'request': self._handle_request,
            'book': self._handle_book,
            'buy': self._handle_buy,
        }

        handler = action_handlers.get(intent['action'], self._handle_default)
        try:
            steps = handler(intent)
        except Exception as e:
            self.logger.error(f"Error generating steps for intent {intent['action']}: {str(e)}")
            steps = [create_step(f"Error handling intent: {intent['action']}")]

        if not steps:
            step_name = f"Default step for {intent['action']}"
            steps.append((step_name, create_step(f"Default step for intent: {intent['action']}")))

        return steps

    def _handle_inform(self, intent):
        steps = []
        steps.append(lambda: print(f"Processing information about {intent.get('subject', 'unknown subject')}"))
        if 'entities' in intent:
            for entity in intent['entities']:
                steps.append(lambda e=entity: print(f"Processing entity: {e['name']} = {e['value']}"))
        return steps

    def _handle_recommend(self, intent):
        steps = []
        steps.append(lambda: print(f"Generating recommendation for {intent.get('object', 'item')}"))
        if 'entities' in intent:
            for entity in intent['entities']:
                steps.append(lambda e=entity: print(f"Considering {e['name']}: {e['value']}"))
        return steps

    def _handle_request(self, intent):
        steps = []
        steps.append(lambda: print(f"Processing request for {intent.get('object', 'unknown object')}"))
        if 'entities' in intent:
            for entity in intent['entities']:
                steps.append(lambda e=entity: print(f"Request parameter: {e['name']} = {e['value']}"))
        return steps

    def _handle_book(self, intent):
        steps = []
        steps.append(lambda: print(f"Booking appointment for {intent.get('object', 'unknown appointment')}"))
        if 'entities' in intent:
            for entity in intent['entities']:
                steps.append(lambda e=entity: print(f"Appointment detail: {e['name']} = {e['value']}"))
        return steps

    def _handle_buy(self, intent):
        steps = []
        steps.append(lambda: print(f"Processing purchase intent for {intent.get('subject', 'unknown item')}"))
        if 'entities' in intent:
            for entity in intent['entities']:
                steps.append(lambda e=entity: print(f"Purchase detail: {e}"))
        steps.append(lambda: print(f"Considering financial aspect: {intent.get('object', 'unknown')}"))
        return steps

    def _handle_default(self, intent):
        return [lambda: print(f"Handling unknown intent action: {intent['action']}")]