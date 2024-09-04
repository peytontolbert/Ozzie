import random
from typing import Dict, List, Tuple

class SimulatedEnvironment:
    def __init__(self, size: Tuple[int, int, int] = (100, 100, 50)):
        self.size = size
        self.obstacles = self._generate_obstacles()
        self.weather = self._generate_weather()
        self.drones = {}
        self.packages = {}

    def _generate_obstacles(self) -> List[Dict]:
        num_obstacles = random.randint(10, 30)
        return [
            {
                "type": random.choice(["building", "tree", "powerline"]),
                "position": (
                    random.randint(0, self.size[0]),
                    random.randint(0, self.size[1]),
                    random.randint(0, self.size[2])
                ),
                "size": random.randint(1, 10)
            }
            for _ in range(num_obstacles)
        ]

    def _generate_weather(self) -> Dict:
        return {
            "wind_speed": random.uniform(0, 20),
            "wind_direction": random.uniform(0, 360),
            "precipitation": random.choice(["none", "light", "moderate", "heavy"]),
            "visibility": random.uniform(0, 10)
        }

    def add_drone(self, drone_id: str, initial_position: Tuple[int, int, int]):
        self.drones[drone_id] = {
            "position": initial_position,
            "battery": 100,
            "status": "idle"
        }

    def add_package(self, package_id: str, pickup: Tuple[int, int, int], delivery: Tuple[int, int, int]):
        self.packages[package_id] = {
            "pickup": pickup,
            "delivery": delivery,
            "status": "waiting"
        }

    def move_drone(self, drone_id: str, direction: Tuple[int, int, int]) -> Dict:
        if drone_id not in self.drones:
            return {"success": False, "message": "Drone not found"}

        new_position = tuple(a + b for a, b in zip(self.drones[drone_id]["position"], direction))
        
        # Check for collisions with obstacles
        for obstacle in self.obstacles:
            if self._check_collision(new_position, obstacle):
                return {"success": False, "message": f"Collision with {obstacle['type']}"}

        # Check if the drone is within the environment boundaries
        if not all(0 <= p <= s for p, s in zip(new_position, self.size)):
            return {"success": False, "message": "Out of bounds"}

        # Update drone position and battery
        self.drones[drone_id]["position"] = new_position
        self.drones[drone_id]["battery"] -= 1

        return {"success": True, "message": "Moved successfully"}

    def _check_collision(self, position: Tuple[int, int, int], obstacle: Dict) -> bool:
        return all(abs(a - b) <= obstacle["size"] for a, b in zip(position, obstacle["position"]))

    def pickup_package(self, drone_id: str, package_id: str) -> Dict:
        if drone_id not in self.drones or package_id not in self.packages:
            return {"success": False, "message": "Drone or package not found"}

        if self.packages[package_id]["status"] != "waiting":
            return {"success": False, "message": "Package not available for pickup"}

        if self.drones[drone_id]["position"] != self.packages[package_id]["pickup"]:
            return {"success": False, "message": "Drone not at pickup location"}

        self.packages[package_id]["status"] = "in_transit"
        self.drones[drone_id]["status"] = "carrying"

        return {"success": True, "message": "Package picked up successfully"}

    def deliver_package(self, drone_id: str, package_id: str) -> Dict:
        if drone_id not in self.drones or package_id not in self.packages:
            return {"success": False, "message": "Drone or package not found"}

        if self.packages[package_id]["status"] != "in_transit":
            return {"success": False, "message": "Package not in transit"}

        if self.drones[drone_id]["position"] != self.packages[package_id]["delivery"]:
            return {"success": False, "message": "Drone not at delivery location"}

        self.packages[package_id]["status"] = "delivered"
        self.drones[drone_id]["status"] = "idle"

        return {"success": True, "message": "Package delivered successfully"}

    def get_environment_state(self) -> Dict:
        return {
            "drones": self.drones,
            "packages": self.packages,
            "weather": self.weather,
            "obstacles": self.obstacles
        }

    def update_weather(self):
        self.weather = self._generate_weather()