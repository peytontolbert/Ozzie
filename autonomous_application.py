import asyncio
from chat_with_ollama import ChatGPT
from agent_communication import Message, communication_hub
from utils.logger import Logger

class AutonomousApplication:
    def __init__(self, name, purpose, role="Worker", query_engine=None):
        self.name = name
        self.purpose = purpose
        self.chat_gpt = ChatGPT()
        self.state = {}
        self.skills = []
        self.role = role
        self.subordinates = []
        self.manager = None
        self.logger = Logger(name)
        communication_hub.register_agent(self.name)
        self.query_engine = query_engine

    async def run(self):
        while True:
            await self.check_messages()
            action = await self.decide_action()
            result = await self.execute_action(action)
            await self.process_result(result)
            await self.learn_new_skill()
            await asyncio.sleep(1)

    async def check_messages(self):
        message = await communication_hub.receive_message(self.name)
        if message:
            await self.process_message(message)

    async def process_message(self, message: Message):
        if message.content.startswith("TASK:"):
            task = message.content[5:]
            result = await self.execute_action(task)
            await self.send_message(message.sender, f"RESULT: {result}")
        elif message.content.startswith("REPORT:"):
            self.logger.info(f"Received report from {message.sender}: {message.content[7:]}")

    async def send_message(self, receiver: str, content: str):
        message = Message(self.name, receiver, content)
        await communication_hub.send_message(message)

    async def decide_action(self):
        if self.role == "Manager":
            return await self.decide_manager_action()
        else:
            return await self.decide_worker_action()

    async def decide_manager_action(self):
        prompt = f"As {self.name}, a manager with the purpose of {self.purpose}, what action should I take next? Current state: {self.state}, Subordinates: {self.subordinates}"
        response = await self.chat_gpt.chat_with_ollama(prompt)
        return response

    async def decide_worker_action(self):
        prompt = f"As {self.name}, a worker with the purpose of {self.purpose}, what action should I take next? Current state: {self.state}, Available skills: {self.skills}"
        response = await self.chat_gpt.chat_with_ollama(prompt)
        return response

    async def execute_action(self, action):
        if action.startswith("ASSIGN_TASK:"):
            _, subordinate, task = action.split(":", 2)
            await self.send_message(subordinate, f"TASK:{task}")
            return f"Assigned task to {subordinate}"
        elif action.startswith("REPORT:"):
            if self.manager:
                await self.send_message(self.manager, action)
                return "Reported to manager"
            else:
                return "No manager to report to"
        else:
            # Implement other action execution logic here
            return f"Executed: {action}"

    async def process_result(self, result):
        prompt = f"Given the result '{result}', how should I update my state and what should I learn from this?"
        response = await self.chat_gpt.chat_with_ollama(prompt)
        # Update state based on the response
        self.state['last_action_result'] = result
        self.state['learned'] = response

    async def learn_new_skill(self):
        prompt = f"Based on my purpose '{self.purpose}' and current skills {self.skills}, suggest a new skill I should learn."
        response = await self.chat_gpt.chat_with_ollama(prompt)
        self.skills.append(response)
        self.logger.info(f"{self.name} learned a new skill: {response}")
        
        if self.query_engine:
            self.query_engine.add_entity(f"Skill_{response}", {"name": response, "agent": self.name})
            self.query_engine.add_relationship(self.name, f"Skill_{response}", "HAS_SKILL")

    def add_subordinate(self, subordinate_name):
        self.subordinates.append(subordinate_name)

    def set_manager(self, manager_name):
        self.manager = manager_name