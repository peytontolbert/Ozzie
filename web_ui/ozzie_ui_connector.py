import aiohttp
import asyncio
from typing import Dict, Any

class OzzieUIConnector:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = None

    async def connect(self):
        self.session = aiohttp.ClientSession()

    async def disconnect(self):
        if self.session:
            await self.session.close()

    async def fetch_data(self, endpoint: str) -> Dict[str, Any]:
        if not self.session:
            raise Exception("Connection not established. Call connect() first.")
        
        async with self.session.get(f"{self.base_url}/{endpoint}") as response:
            return await response.json()

    async def send_data(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.session:
            raise Exception("Connection not established. Call connect() first.")
        
        async with self.session.post(f"{self.base_url}/{endpoint}", json=data) as response:
            return await response.json()

    async def update_data(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.session:
            raise Exception("Connection not established. Call connect() first.")
        
        async with self.session.put(f"{self.base_url}/{endpoint}", json=data) as response:
            return await response.json()

# Usage example
async def main():
    connector = OzzieUIConnector("http://localhost:8000/api")
    await connector.connect()
    
    try:
        data = await connector.fetch_data("dashboard-data")
        print("Dashboard data:", data)
        
        new_task = {"title": "New Task", "description": "This is a new task"}
        result = await connector.send_data("tasks", new_task)
        print("New task created:", result)
        
        update_data = {"id": result["task_id"], "status": "In Progress"}
        updated = await connector.update_data(f"tasks/{result['task_id']}", update_data)
        print("Task updated:", updated)
    
    finally:
        await connector.disconnect()

if __name__ == "__main__":
    asyncio.run(main())