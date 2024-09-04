import os
from utils.logger import Logger

class VersionControl:
    def __init__(self):
        self.logger = Logger("VersionControl")
        self.base_path = "project_versions"

    def initialize(self):
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
        self.logger.info("Version control system initialized")

    def commit(self, project, task, code):
        project_path = os.path.join(self.base_path, project.name)
        if not os.path.exists(project_path):
            os.makedirs(project_path)
        
        version = len(os.listdir(project_path)) + 1
        file_name = f"v{version}_{task.name}.py"
        file_path = os.path.join(project_path, file_name)
        
        with open(file_path, 'w') as f:
            f.write(code)
        
        self.logger.info(f"Committed version {version} for task {task.name} in project {project.name}")

    def get_latest_version(self, project, task):
        project_path = os.path.join(self.base_path, project.name)
        if not os.path.exists(project_path):
            return None
        
        versions = [f for f in os.listdir(project_path) if f.endswith(f"{task.name}.py")]
        if not versions:
            return None
        
        latest_version = max(versions)
        file_path = os.path.join(project_path, latest_version)
        
        with open(file_path, 'r') as f:
            return f.read()