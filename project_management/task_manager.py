from utils.logger import Logger

class TaskManager:
    def __init__(self):
        self.logger = Logger("TaskManager")

    def create_initial_tasks(self, project):
        # For simplicity, let's create a single initial task
        task = Task("initial_task", "Implement basic project structure")
        project.add_task(task)
        self.logger.info(f"Created initial task for project {project.name}")

    def get_next_task(self, project):
        return project.get_next_task()

    def complete_task(self, task):
        task.complete()
        self.logger.info(f"Completed task: {task.name}")

class Task:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.is_completed = False

    def complete(self):
        self.is_completed = True