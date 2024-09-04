from typing import Dict, Any, List
import numpy as np
import random
from collections import defaultdict

class FeedbackIntegrator:
    def __init__(self, state_size=10, action_size=5):  # Add default values
        self.feedback_history = []
        self.learning_rate = 0.1
        self.reinforcement_learning_module = ReinforcementLearningModule(state_size, action_size)
        self.active_learning_engine = ActiveLearningEngine(self)  # Assuming ActiveLearningEngine needs the FeedbackIntegrator instance

    def integrate(self, result: Dict[str, Any], impact: Dict[str, float], is_aligned: bool):
        feedback = self._process_feedback(result, impact, is_aligned)
        self._update_model(feedback)
        self._store_feedback(feedback)

    def _process_feedback(self, result: Dict[str, Any], impact: Dict[str, float], is_aligned: bool) -> Dict[str, Any]:
        feedback = {
            "result": result,
            "impact": impact,
            "is_aligned": is_aligned,
            "sentiment": np.mean(list(impact.values())) if impact else 0,
            "importance": sum(impact.values()) / len(impact) if impact else 0
        }
        return feedback

    def _update_model(self, feedback: Dict[str, Any]):
        # This is a placeholder for actual model updating logic
        # In a real system, this would update the AI's decision-making model
        if feedback["is_aligned"]:
            self.learning_rate *= 1.1  # Increase learning rate for aligned actions
        else:
            self.learning_rate *= 0.9  # Decrease learning rate for misaligned actions
        
        print(f"Model updated based on feedback. New learning rate: {self.learning_rate}")

    def _store_feedback(self, feedback: Dict[str, Any]):
        self.feedback_history.append(feedback)
        if len(self.feedback_history) > 1000:  # Limit history to last 1000 items
            self.feedback_history.pop(0)

    def analyze_feedback_trends(self) -> str:
        if not self.feedback_history:
            return "No feedback history available."

        positive_count = sum(1 for item in self.feedback_history if item['sentiment'] > 0)
        negative_count = sum(1 for item in self.feedback_history if item['sentiment'] < 0)
        neutral_count = len(self.feedback_history) - positive_count - negative_count

        trend_analysis = f"Feedback Trend Analysis:\n"
        trend_analysis += f"Positive feedback: {positive_count}\n"
        trend_analysis += f"Negative feedback: {negative_count}\n"
        trend_analysis += f"Neutral feedback: {neutral_count}\n"

        return trend_analysis

    def get_recent_feedback(self, n: int = 5) -> List[Dict[str, Any]]:
        return self.feedback_history[-n:]

# Add new classes for advanced feedback integration
class ReinforcementLearningModule:
    def __init__(self, state_size=10, action_size=5, learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        self.q_table = defaultdict(lambda: np.zeros(action_size))
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.action_size = action_size

    def update(self, state, action, reward, next_state):
        current_q = self.q_table[state][action]
        next_max_q = np.max(self.q_table[next_state])
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_max_q - current_q)
        self.q_table[state][action] = new_q

    def get_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.action_size)
        return np.argmax(self.q_table[state])

class ActiveLearningEngine:
    def __init__(self, feedback_integrator, uncertainty_threshold=0.3):
        self.feedback_integrator = feedback_integrator
        self.uncertainty_threshold = uncertainty_threshold
        self.labeled_data = []

    def learn(self, unlabeled_data):
        uncertain_samples = []
        for sample in unlabeled_data:
            uncertainty = self._calculate_uncertainty(sample)
            if uncertainty > self.uncertainty_threshold:
                label = self._query_oracle(sample)
                self.labeled_data.append((sample, label))
                uncertain_samples.append(sample)
        
        if uncertain_samples:
            self._update_model(uncertain_samples)

    def _calculate_uncertainty(self, sample):
        # Placeholder: In a real scenario, this would use the model to predict
        # and calculate uncertainty based on prediction probabilities
        return np.random.random()

    def _query_oracle(self, sample):
        # Placeholder: In a real scenario, this would involve human interaction
        return np.random.randint(2)

    def _update_model(self, new_samples):
        # Placeholder: In a real scenario, this would retrain the model
        print(f"Updating model with {len(new_samples)} new samples")

# Usage example
if __name__ == "__main__":
    integrator = FeedbackIntegrator()
    
    # Simulate some feedback
    for _ in range(10):
        result = {"action": "Test action", "outcome": "Success" if np.random.random() > 0.5 else "Failure"}
        impact = {"Environmental": np.random.uniform(-1, 1), "Social": np.random.uniform(-1, 1)}
        is_aligned = np.random.random() > 0.3
        
        integrator.integrate(result, impact, is_aligned)
    
    print(integrator.analyze_feedback_trends())
    print("Recent feedback:", integrator.get_recent_feedback(3))