import asyncio
from base.base_workflow import BaseWorkflow
from tasks.task_queue import TaskQueue
from functools import lru_cache
import json
from base.concrete_workflow import ConcreteWorkflow
from utils.logger import Logger
from utils.error_handler import ErrorHandler
from chat_with_ollama import ChatGPT

class WorkflowEngine:
    def __init__(self):
        self.workflows = {}
        self.task_queue = TaskQueue()
        self.logger = Logger("WorkflowEngine")
        self.error_handler = ErrorHandler()
        self.chat_gpt = ChatGPT()

    def register_workflow(self, workflow_name, workflow):
        if not isinstance(workflow, BaseWorkflow):
            raise TypeError("Workflow must be an instance of BaseWorkflow")
        self.workflows[workflow_name] = workflow

    async def execute_workflow(self, workflow_name, *args, **kwargs):
        if workflow_name not in self.workflows:
            raise ValueError(f"Workflow '{workflow_name}' not found")
        
        workflow = self.workflows[workflow_name]
        results = []
        for step in workflow.steps:
            try:
                if asyncio.iscoroutinefunction(step):
                    result = await step(*args, **kwargs)
                else:
                    result = step(*args, **kwargs)
                results.append(result)
            except Exception as e:
                self.error_handler.handle_error(e, f"Error executing task in workflow {workflow_name}")
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

    async def generate_workflow(self, intent_str):
        try:
            # Parse the intent string
            intent = json.loads(intent_str)
            
            # Generate steps based on the intent
            steps = await self._generate_steps(intent)
            
            if not steps:
                self.logger.warning("No steps generated for workflow.")
                return None
            
            # Create and return a new ConcreteWorkflow instance
            workflow_name = f"Workflow for {intent.get('action', 'unknown_action')}"
            workflow = ConcreteWorkflow(name=workflow_name, steps=steps)
            self.register_workflow(workflow_name, workflow)
            return workflow
        except json.JSONDecodeError:
            self.error_handler.handle_error("Invalid JSON in intent string", "Error generating workflow")
            return None
        except Exception as e:
            self.error_handler.handle_error(e, f"Error generating workflow: {str(e)}")
            return None

    async def _generate_steps(self, intent):
        intent_str = json.dumps(intent, indent=2)
        prompt = f"""Generate a list of steps for a workflow based on the following intent:
        {intent_str}
        
        Each step should be a brief description of an action to take.
        """
        response = await self.chat_gpt.chat_with_ollama(prompt)
        if response.startswith("Error:"):
            self.logger.warning(f"Failed to generate workflow steps: {response}")
            return [self._create_step("Default action")]
        steps = response.strip().split('\n')
        return [self._create_step(step) for step in steps]

    def _create_step(self, description):
        return lambda: {"message": description, "action_suggestion": {"type": "default_action"}}

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

    def _create_autonomous_application_workflow(self):
        return [
            self._create_step("Define application purpose"),
            self._create_step("Generate application name"),
            self._create_step("Create autonomous application"),
            self._create_step("Initialize application state"),
            self._create_step("Start application execution")
        ]