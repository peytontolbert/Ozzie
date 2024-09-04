from typing import Dict, Any, List
import numpy as np

class FeedbackIntegrator:
    def __init__(self):
        self.feedback_history = []
        self.learning_rate = 0.1

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