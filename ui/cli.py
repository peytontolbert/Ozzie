import cmd
import sys
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class OzzieCLI(cmd.Cmd):
    intro = "Welcome to Ozzie CLI. Type help or ? to list commands.\n"
    prompt = "(ozzie) "

    def __init__(self, ozzie_agent):
        super().__init__()
        self.ozzie = ozzie_agent
        self.logger = Logger("OzzieCLI")
        self.error_handler = ErrorHandler()

    def do_status(self, arg):
        """Get the current status of Ozzie"""
        try:
            status = self.ozzie.get_status()
            print(f"Ozzie's current status: {status}")
        except Exception as e:
            self.error_handler.handle_error(e, "Error getting Ozzie's status")

    def do_execute_workflow(self, arg):
        """Execute a workflow. Usage: execute_workflow <workflow_name>"""
        try:
            workflow_name = arg.strip()
            if not workflow_name:
                print("Please provide a workflow name.")
                return
            result = self.ozzie.execute_workflow(workflow_name)
            print(f"Workflow execution result: {result}")
        except Exception as e:
            self.error_handler.handle_error(e, f"Error executing workflow: {arg}")

    def do_list_workflows(self, arg):
        """List all available workflows"""
        try:
            workflows = self.ozzie.list_workflows()
            print("Available workflows:")
            for workflow in workflows:
                print(f"- {workflow}")
        except Exception as e:
            self.error_handler.handle_error(e, "Error listing workflows")

    def do_exit(self, arg):
        """Exit the CLI"""
        print("Thank you for using Ozzie CLI. Goodbye!")
        return True

    def default(self, line):
        self.logger.warning(f"Unknown command: {line}")
        print(f"Unknown command: {line}")

def run_cli(ozzie_agent):
    OzzieCLI(ozzie_agent).cmdloop()

if __name__ == "__main__":
    # This is for testing purposes. In production, you'd pass the actual Ozzie agent.
    class MockOzzie:
        def get_status(self):
            return "Operational"
        def execute_workflow(self, name):
            return f"Executed workflow: {name}"
        def list_workflows(self):
            return ["workflow1", "workflow2", "workflow3"]

    run_cli(MockOzzie())