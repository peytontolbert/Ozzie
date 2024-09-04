import numpy as np
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class AdaptiveGoalSetting:
    def __init__(self):
        self.logger = Logger("AdaptiveGoalSetting")
        self.error_handler = ErrorHandler()
        self.goals = []
        self.performance_history = []

    def add_goal(self, goal, priority=1.0):
        try:
            self.goals.append({'description': goal, 'priority': priority, 'progress': 0.0})
            self.logger.info(f"Added new goal: {goal}")
        except Exception as e:
            self.error_handler.handle_error(e, f"Error adding goal: {goal}")

    def update_goal_progress(self, goal_index, progress):
        try:
            if 0 <= goal_index < len(self.goals):
                self.goals[goal_index]['progress'] = progress
                self.logger.info(f"Updated progress for goal {goal_index}: {progress}")
            else:
                raise ValueError("Invalid goal index")
        except Exception as e:
            self.error_handler.handle_error(e, f"Error updating goal progress for index {goal_index}")

    def prioritize_goals(self):
        try:
            self.goals.sort(key=lambda x: (1 - x['progress']) * x['priority'], reverse=True)
            self.logger.info("Goals prioritized")
        except Exception as e:
            self.error_handler.handle_error(e, "Error prioritizing goals")

    def generate_new_goal(self, current_state, desired_state):
        try:
            difference = np.array(desired_state) - np.array(current_state)
            most_significant_aspect = np.argmax(np.abs(difference))
            new_goal = f"Improve {most_significant_aspect} by {difference[most_significant_aspect]:.2f}"
            self.add_goal(new_goal)
            return new_goal
        except Exception as e:
            self.error_handler.handle_error(e, "Error generating new goal")
            return None

    def adapt_goals(self, performance):
        try:
            self.performance_history.append(performance)
            if len(self.performance_history) > 10:
                self.performance_history.pop(0)
            
            avg_performance = np.mean(self.performance_history)
            if performance < avg_performance:
                # Simplify goals if performance is declining
                self.goals = self.goals[:max(1, len(self.goals) - 1)]
                self.logger.info("Simplified goals due to declining performance")
            elif performance > avg_performance and len(self.goals) < 5:
                # Add a new goal if performance is improving
                new_goal = self.generate_new_goal(self.performance_history[-2:], [performance * 1.1])
                self.logger.info(f"Added new goal due to improving performance: {new_goal}")
        except Exception as e:
            self.error_handler.handle_error(e, "Error adapting goals")

    def get_current_goal(self):
        try:
            self.prioritize_goals()
            return self.goals[0] if self.goals else None
        except Exception as e:
            self.error_handler.handle_error(e, "Error getting current goal")
            return None

    def evaluate_goal_achievement(self):
        try:
            achieved_goals = [goal for goal in self.goals if goal['progress'] >= 1.0]
            for goal in achieved_goals:
                self.logger.info(f"Goal achieved: {goal['description']}")
                self.goals.remove(goal)
            return len(achieved_goals)
        except Exception as e:
            self.error_handler.handle_error(e, "Error evaluating goal achievement")
            return 0