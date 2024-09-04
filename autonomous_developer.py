import asyncio
from chat_with_ollama import ChatGPT
from skills.coding_skills import CodingSkills
from project_management.project import Project, Task
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class AutonomousDeveloper:
    def __init__(self, agi_components):
        self.chat_gpt = ChatGPT()
        self.coding_skills = CodingSkills(agi_components)
        self.logger = Logger("AutonomousDeveloper")
        self.error_handler = ErrorHandler()
        self.current_project = None

    async def start_project(self, project_description):
        try:
            project_details = await self.chat_gpt.chat_with_ollama(
                system_prompt="You are a project manager. Create a project plan based on the given description.",
                prompt=f"Create a project plan for: {project_description}"
            )
            project_name = project_details.get('name', 'Unnamed Project')
            self.current_project = Project(project_name, project_description)
            
            for task in project_details.get('tasks', []):
                self.current_project.add_task(Task(task['name'], task['description']))
            
            self.logger.info(f"Started new project: {project_name}")
            return self.current_project
        except Exception as e:
            self.error_handler.handle_error(e, "Error starting project")
            return None

    async def develop(self):
        while self.current_project and not self.current_project.is_completed():
            task = self.current_project.get_next_task()
            if task:
                await self.execute_task(task)
            else:
                await asyncio.sleep(1)  # Wait for new tasks

    async def execute_task(self, task):
        try:
            code = await self.coding_skills.generate_code(task.description)
            review_result = await self.coding_skills.review_code(code)
            
            if review_result['approved']:
                task.complete(code)
                self.logger.info(f"Completed task: {task.name}")
            else:
                refactored_code = await self.coding_skills.refactor_code(code, review_result['feedback'])
                task.complete(refactored_code)
                self.logger.info(f"Completed task after refactoring: {task.name}")
            
            self.current_project.update_status()
        except Exception as e:
            self.error_handler.handle_error(e, f"Error executing task: {task.name}")

    async def get_project_status(self):
        if self.current_project:
            return {
                "name": self.current_project.name,
                "description": self.current_project.description,
                "status": self.current_project.status,
                "completed_tasks": len([t for t in self.current_project.tasks if t.is_completed]),
                "total_tasks": len(self.current_project.tasks)
            }
        return None