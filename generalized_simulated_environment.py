import random
from typing import Dict, List, Tuple, Any
from abc import ABC, abstractmethod

class Entity(ABC):
    def __init__(self, entity_id: str, position: Tuple[float, float, float]):
        self.id = entity_id
        self.position = position
        self.properties = {}

    @abstractmethod
    def update(self, environment: 'GeneralizedSimulatedEnvironment'):
        pass

class GeneralizedSimulatedEnvironment:
    def __init__(self, size: Tuple[float, float, float] = (100.0, 100.0, 100.0)):
        self.size = size
        self.entities: Dict[str, Entity] = {}
        self.global_properties: Dict[str, Any] = {}
        self.time = 0

    def add_entity(self, entity: Entity):
        self.entities[entity.id] = entity

    def remove_entity(self, entity_id: str):
        if entity_id in self.entities:
            del self.entities[entity_id]

    def get_entity(self, entity_id: str) -> Entity:
        return self.entities.get(entity_id)

    def set_global_property(self, key: str, value: Any):
        self.global_properties[key] = value

    def get_global_property(self, key: str) -> Any:
        return self.global_properties.get(key)

    def update(self):
        self.time += 1
        for entity in self.entities.values():
            entity.update(self)

    def get_entities_in_range(self, position: Tuple[float, float, float], range: float) -> List[Entity]:
        return [
            entity for entity in self.entities.values()
            if self.calculate_distance(position, entity.position) <= range
        ]

    @staticmethod
    def calculate_distance(pos1: Tuple[float, float, float], pos2: Tuple[float, float, float]) -> float:
        return sum((a - b) ** 2 for a, b in zip(pos1, pos2)) ** 0.5

    def is_position_valid(self, position: Tuple[float, float, float]) -> bool:
        return all(0 <= p <= s for p, s in zip(position, self.size))

    def get_environment_state(self) -> Dict:
        return {
            "time": self.time,
            "global_properties": self.global_properties,
            "entities": {entity_id: entity.__dict__ for entity_id, entity in self.entities.items()}
        }

# Example entity types (can be extended for different scenarios)

class Agent(Entity):
    def __init__(self, agent_id: str, position: Tuple[float, float, float]):
        super().__init__(agent_id, position)
        self.properties["status"] = "idle"

    def update(self, environment: GeneralizedSimulatedEnvironment):
        # Implement agent behavior here
        pass

class Obstacle(Entity):
    def __init__(self, obstacle_id: str, position: Tuple[float, float, float], size: float):
        super().__init__(obstacle_id, position)
        self.properties["size"] = size

    def update(self, environment: GeneralizedSimulatedEnvironment):
        # Obstacles typically don't need updating, but the method is required
        pass

class Resource(Entity):
    def __init__(self, resource_id: str, position: Tuple[float, float, float], resource_type: str):
        super().__init__(resource_id, position)
        self.properties["type"] = resource_type
        self.properties["available"] = True

    def update(self, environment: GeneralizedSimulatedEnvironment):
        # Implement resource behavior (e.g., regeneration) here
        pass