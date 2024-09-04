import git
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class Task:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.is_completed = False
        self.code = None

    def complete(self, code):
        self.is_completed = True
        self.code = code

class Project:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.tasks = []
        self.status = "In Progress"

    def add_task(self, task):
        self.tasks.append(task)

    def get_next_task(self):
        for task in self.tasks:
            if not task.is_completed:
                return task
        return None

    def update_status(self):
        if all(task.is_completed for task in self.tasks):
            self.status = "Completed"
        else:
            self.status = "In Progress"

    def is_completed(self):
        return self.status == "Completed"

class ProjectManager:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.repo = git.Repo(repo_path)
        self.logger = Logger("ProjectManager")
        self.error_handler = ErrorHandler()
        self.projects = []

    async def create_project(self, name, description):
        project = Project(name, description)
        self.projects.append(project)
        return project

    async def get_next_project(self):
        for project in self.projects:
            if not project.is_completed():
                return project
        return None

    async def commit_code(self, code, task):
        try:
            file_path = self._determine_file_path(task)
            with open(file_path, 'w') as f:
                f.write(code)
            self.repo.index.add([file_path])
            self.repo.index.commit(f"Implement {task.name}")
            self.logger.info(f"Committed code for task: {task.name}")
        except Exception as e:
            self.error_handler.handle_error(e, f"Error committing code for task: {task.name}")

    def _determine_file_path(self, task):
        # Implement logic to determine appropriate file path based on the task
        return f"{self.repo_path}/auto_generated_{task.name.replace(' ', '_')}.py"