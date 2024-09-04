import json
import os

class WorkflowLibrary:
    def __init__(self, storage_path):
        self.storage_path = storage_path
        self.workflows = {}
        self.load_workflows()

    def load_workflows(self):
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
        for filename in os.listdir(self.storage_path):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(self.storage_path, filename), 'r') as f:
                        workflow_data = json.load(f)
                        self.workflows[workflow_data['name']] = workflow_data
                except json.JSONDecodeError:
                    print(f"Error loading workflow from {filename}")

    def save_workflow(self, workflow):
        workflow_data = {
            'name': workflow.name,
            'steps': [step.__name__ for step in workflow.steps]
        }
        filename = f"{workflow.name}.json"
        try:
            with open(os.path.join(self.storage_path, filename), 'w') as f:
                json.dump(workflow_data, f, indent=2)
            self.workflows[workflow.name] = workflow_data
            return True
        except IOError:
            print(f"Error saving workflow {workflow.name}")
            return False

    def get_workflow(self, name):
        return self.workflows.get(name)

    def list_workflows(self):
        return list(self.workflows.keys())

    def delete_workflow(self, name):
        if name in self.workflows:
            del self.workflows[name]
            filename = f"{name}.json"
            try:
                os.remove(os.path.join(self.storage_path, filename))
                return True
            except OSError:
                print(f"Error deleting workflow file for {name}")
        return False

    def update_workflow(self, workflow):
        if workflow.name in self.workflows:
            return self.save_workflow(workflow)
        return False