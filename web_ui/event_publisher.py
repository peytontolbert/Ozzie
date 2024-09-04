import asyncio
from typing import Dict, Any, List, Callable

class EventPublisher:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_queue: asyncio.Queue = asyncio.Queue()

    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable):
        if event_type in self.subscribers and callback in self.subscribers[event_type]:
            self.subscribers[event_type].remove(callback)

    async def publish(self, event_type: str, data: Any):
        await self.event_queue.put((event_type, data))

    async def process_events(self):
        while True:
            event_type, data = await self.event_queue.get()
            if event_type in self.subscribers:
                for callback in self.subscribers[event_type]:
                    await callback(data)
            self.event_queue.task_done()

    async def start(self):
        asyncio.create_task(self.process_events())

event_publisher = EventPublisher()