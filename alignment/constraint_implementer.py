from utils.logger import Logger
from utils.error_handler import ErrorHandler

class ConstraintImplementer:
    def __init__(self):
        self.constraints = {}
        self.logger = Logger("ConstraintImplementer")
        self.error_handler = ErrorHandler()

    def add_constraint(self, constraint_name, constraint_function):
        try:
            self.constraints[constraint_name] = constraint_function
            self.logger.info(f"Added constraint: {constraint_name}")
        except Exception as e:
            self.error_handler.handle_error(e, f"Error adding constraint: {constraint_name}")

    def remove_constraint(self, constraint_name):
        try:
            del self.constraints[constraint_name]
            self.logger.info(f"Removed constraint: {constraint_name}")
        except KeyError:
            self.logger.warning(f"Constraint not found: {constraint_name}")
        except Exception as e:
            self.error_handler.handle_error(e, f"Error removing constraint: {constraint_name}")

    def apply_constraints(self, agent_action):
        try:
            for constraint_name, constraint_function in self.constraints.items():
                agent_action = constraint_function(agent_action)
            return agent_action
        except Exception as e:
            self