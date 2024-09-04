import random
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class NLGenerator:
    def __init__(self):
        self.logger = Logger("NLGenerator")
        self.error_handler = ErrorHandler()
        self.templates = {
            'greeting': [
                "Hello, {name}!",
                "Hi there, {name}!",
                "Greetings, {name}!"
            ],
            'task_complete': [
                "I've finished the task: {task}",
                "The task '{task}' is now complete.",
                "Task completed: {task}"
            ],
            'error': [
                "An error occurred: {error}",
                "Oops! Something went wrong: {error}",
                "I encountered an issue: {error}"
            ]
        }

    def generate(self, template_type, **kwargs):
        try:
            if template_type not in self.templates:
                raise ValueError(f"Unknown template type: {template_type}")

            template = random.choice(self.templates[template_type])
            return template.format(**kwargs)
        except Exception as e:
            self.error_handler.handle_error(e, "Error generating text")
            return None

    def add_template(self, template_type, templates):
        try:
            if not isinstance(templates, list):
                templates = [templates]
            if template_type in self.templates:
                self.templates[template_type].extend(templates)
            else:
                self.templates[template_type] = templates
            self.logger.info(f"Added new template(s) for {template_type}")
        except Exception as e:
            self.error_handler.handle_error(e, "Error adding template")

    def generate_response(self, input_text):
        # This is a placeholder for more complex response generation
        try:
            words = input_text.lower().split()
            if "hello" in words or "hi" in words:
                return self.generate('greeting', name="User")
            elif "task" in words and "complete" in words:
                return self.generate('task_complete', task="requested task")
            else:
                return "I'm not sure how to respond to that."
        except Exception as e:
            self.error_handler.handle_error(e, "Error generating response")
            return "I'm sorry, I couldn't generate a response."