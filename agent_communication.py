import asyncio
from typing import Dict, List, Any
import json

class Message:
    def __init__(self, sender: str, receiver: str, content: Any, message_type: str):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.message_type = message_type

class CommunicationHub:
    def __init__(self):
        self.message_queues: Dict[str, asyncio.Queue] = {}

    def register_agent(self, agent_id: str):
        if agent_id not in self.message_queues:
            self.message_queues[agent_id] = asyncio.Queue()

    async def send_message(self, message: Message):
        if message.receiver in self.message_queues:
            await self.message_queues[message.receiver].put(message)
        else:
            print(f"Error: Recipient {message.receiver} not found")

    async def receive_message(self, agent_id: str) -> Message:
        if agent_id in self.message_queues:
            return await self.message_queues[agent_id].get()
        else:
            print(f"Error: Agent {agent_id} not registered")
            return None

communication_hub = CommunicationHub()