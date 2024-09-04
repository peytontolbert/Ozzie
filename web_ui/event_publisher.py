import asyncio
from typing import Dict, Any

class EventPublisher:
    def __init__(self):
        self.subscribers = {}

    async def start(self):
        # Any initialization logic can go here
        pass

    async def publish(self, event_type: str, data: Dict[str, Any]):
        if event_type in self.subscribers:
            for subscriber in self.subscribers[event_type]:
                await subscriber(data)

    def subscribe(self, event_type: str, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback):
        if event_type in self.subscribers:
            self.subscribers[event_type].remove(callback)

event_publisher = EventPublisher()