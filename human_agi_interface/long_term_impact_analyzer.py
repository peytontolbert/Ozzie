from typing import Dict, Any, List, Union
import numpy as np
from scipy.stats import norm
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class ImpactCategory:
    def __init__(self, name: str, weight: float):
        self.name = name
        self.weight = weight

class LongTermImpactAnalyzer:
    def __init__(self):
        self.impact_categories = self._initialize_impact_categories()
        self.logger = Logger("LongTermImpactAnalyzer")
        self.error_handler = ErrorHandler()

    def _initialize_impact_categories(self) -> List[ImpactCategory]:
        return [
            ImpactCategory("Environmental", 0.3),
            ImpactCategory("Social", 0.3),
            ImpactCategory("Economic", 0.2),
            ImpactCategory("Technological", 0.2)
        ]

    def analyze(self, action: Union[Dict[str, Any], str], time_horizon: int = 10) -> Dict[str, float]:
        try:
            impacts = {}
            action_name = self._extract_action_name(action)
            for category in self.impact_categories:
                # Simulate impact using a normal distribution
                mean_impact = self._calculate_mean_impact(category.name, action_name)
                std_dev = 0.1  # Fixed standard deviation for simplicity
                impact_distribution = norm(mean_impact, std_dev)
                
                # Calculate cumulative impact over time
                cumulative_impact = sum(impact_distribution.rvs() for _ in range(time_horizon))
                weighted_impact = cumulative_impact * category.weight
                
                impacts[category.name] = weighted_impact

            return impacts
        except Exception as e:
            self.error_handler.handle_error(e, f"Error analyzing long-term impact for action: {action}")
            return {}

    def _extract_action_name(self, action: Union[Dict[str, Any], str]) -> str:
        if isinstance(action, dict):
            return str(action.get('name', action.get('status', str(action))))
        return str(action)

    def _calculate_mean_impact(self, category: str, action: str) -> float:
        # This is a placeholder method. In a real system, you'd implement more sophisticated logic
        # to determine the mean impact based on the category and action.
        return np.random.uniform(-1, 1)

    def visualize_impact(self, impacts: Dict[str, float]):
        try:
            print("Impact Visualization:")
            for category, impact in impacts.items():
                print(f"{category}: {'#' * int(abs(impact) * 10)} ({impact:.2f})")
        except Exception as e:
            self.error_handler.handle_error(e, "Error visualizing impact")

    def generate_impact_report(self, action: Union[Dict[str, Any], str], time_horizon: int = 10) -> str:
        try:
            impacts = self.analyze(action, time_horizon)
            total_impact = sum(impacts.values())
            
            action_name = self._extract_action_name(action)
            report = f"Long-term Impact Analysis for action: {action_name}\n"
            report += f"Time Horizon: {time_horizon} years\n\n"
            
            for category, impact in impacts.items():
                report += f"{category} Impact: {impact:.2f}\n"
            
            report += f"\nTotal Impact: {total_impact:.2f}\n"
            report += f"Overall Assessment: {'Positive' if total_impact > 0 else 'Negative'}\n"
            
            return report
        except Exception as e:
            self.error_handler.handle_error(e, "Error generating impact report")
            return "Error generating impact report"

# Usage example
if __name__ == "__main__":
    analyzer = LongTermImpactAnalyzer()
    action = {"name": "Implement renewable energy policy", "scope": "global"}
    impact_report = analyzer.generate_impact_report(action)
    print(impact_report)
    analyzer.visualize_impact(analyzer.analyze(action))