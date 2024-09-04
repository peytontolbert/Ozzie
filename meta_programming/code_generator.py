import ast
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class CodeGenerator:
    def __init__(self):
        self.logger = Logger("CodeGenerator")
        self.error_handler = ErrorHandler()

    def generate_class(self, class_name, attributes, methods):
        try:
            class_def = f"class {class_name}:\n"
            class_def += "    def __init__(self"
            for attr in attributes:
                class_def += f", {attr}"
            class_def += "):\n"
            for attr in attributes:
                class_def += f"        self.{attr} = {attr}\n"
            class_def += "\n"
            for method_name, method_body in methods.items():
                class_def += f"    def {method_name}(self):\n"
                for line in method_body.split('\n'):
                    class_def += f"        {line}\n"
                class_def += "\n"
            return class_def
        except Exception as e:
            self.error_handler.handle_error(e, f"Error generating class: {class_name}")
            return None

    def generate_function(self, func_name, params, body):
        try:
            func_def = f"def {func_name}({', '.join(params)}):\n"
            for line in body.split('\n'):
                func_def += f"    {line}\n"
            return func_def
        except Exception as e:
            self.error_handler.handle_error(e, f"Error generating function: {func_name}")
            return None

    def generate_workflow(self, workflow_name, steps):
        try:
            workflow_def = f"def {workflow_name}():\n"
            for step in steps:
                workflow_def += f"    {step}\n"
            return workflow_def
        except Exception as e:
            self.error_handler.handle_error(e, f"Error generating workflow: {workflow_name}")
            return None