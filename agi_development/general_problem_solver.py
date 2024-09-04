from utils.logger import Logger
from utils.error_handler import ErrorHandler

class GeneralProblemSolver:
    def __init__(self):
        self.logger = Logger("GeneralProblemSolver")
        self.error_handler = ErrorHandler()

    def define_problem(self, initial_state, goal_state, possible_actions):
        try:
            self.initial_state = initial_state
            self.goal_state = goal_state
            self.possible_actions = possible_actions
            self.logger.info("Problem defined successfully")
        except Exception as e:
            self.error_handler.handle_error(e, "Error defining problem")

    def is_goal_reached(self, state):
        return state == self.goal_state

    def get_possible_actions(self, state):
        return self.possible_actions

    def apply_action(self, state, action):
        try:
            new_state = action(state)
            return new_state
        except Exception as e:
            self.error_handler.handle_error(e, f"Error applying action: {action}")
            return state

    def heuristic(self, state):
        # This is a placeholder heuristic function
        # In a real-world scenario, this would be more sophisticated
        return sum(abs(a - b) for a, b in zip(state, self.goal_state))

    def solve(self):
        try:
            frontier = [(self.initial_state, [])]
            explored = set()

            while frontier:
                state, path = frontier.pop(0)
                
                if self.is_goal_reached(state):
                    return path
                
                explored.add(tuple(state))
                
                for action in self.get_possible_actions(state):
                    new_state = self.apply_action(state, action)
                    if tuple(new_state) not in explored:
                        new_path = path + [action.__name__]
                        frontier.append((new_state, new_path))
                        frontier.sort(key=lambda x: len(x[1]) + self.heuristic(x[0]))

            self.logger.warning("No solution found")
            return None
        except Exception as e:
            self.error_handler.handle_error(e, "Error solving problem")
            return None