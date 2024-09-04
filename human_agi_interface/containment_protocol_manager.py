import logging
from enum import Enum
from typing import Dict, Any, Callable

logger = logging.getLogger(__name__)

class ContainmentLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class ContainmentProtocolManager:
    def __init__(self):
        self.current_level = ContainmentLevel.LOW
        self.protocols: Dict[ContainmentLevel, Callable] = {
            ContainmentLevel.LOW: self._low_protocol,
            ContainmentLevel.MEDIUM: self._medium_protocol,
            ContainmentLevel.HIGH: self._high_protocol,
            ContainmentLevel.CRITICAL: self._critical_protocol
        }

    def activate_protocol(self, level: ContainmentLevel):
        self.current_level = level
        self.protocols[level]()
        logger.info(f"Containment protocol activated: {level.name}")

    def deactivate_protocol(self):
        previous_level = self.current_level
        self.current_level = ContainmentLevel.LOW
        logger.info(f"Containment protocol deactivated from {previous_level.name}")

    def _low_protocol(self):
        # Implement low-level containment measures
        logger.info("Activating low-level containment measures")

    def _medium_protocol(self):
        # Implement medium-level containment measures
        logger.info("Activating medium-level containment measures")

    def _high_protocol(self):
        # Implement high-level containment measures
        logger.info("Activating high-level containment measures")

    def _critical_protocol(self):
        # Implement critical-level containment measures
        logger.info("Activating critical-level containment measures")

    def log_activity(self, activity: Dict[str, Any]):
        logger.info(f"Activity logged: {activity} at containment level {self.current_level.name}")

# Usage example
if __name__ == "__main__":
    manager = ContainmentProtocolManager()
    manager.activate_protocol(ContainmentLevel.MEDIUM)
    manager.log_activity({"action": "test_action", "result": "success"})
    manager.deactivate_protocol()