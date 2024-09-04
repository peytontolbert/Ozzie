from utils.logger import Logger
from utils.error_handler import ErrorHandler
from typing import Dict, Any
import json

class ExplanationGenerator:
    def __init__(self):
        self.explanation_levels = ["simple", "detailed", "technical"]
        self.logger = Logger("ExplanationGenerator")
        self.error_handler = ErrorHandler()

    def generate(self, result, impact, is_aligned):
        explanation = {
            "action_result": {
                "status": result["status"],
                "output": [self._format_output(item) for item in result["output"]],
                "errors": result["errors"],
                "start_time": result["start_time"],
                "end_time": result["end_time"],
                "estimated_runtime": result["estimated_runtime"]
            },
            "impact": impact,
            "alignment": "Aligned" if is_aligned else "Not aligned"
        }
        return json.dumps(explanation, indent=2)

    def _format_output(self, output_item):
        return {
            "name": str(output_item["name"]),
            "status": output_item["status"],
            "output": output_item["output"],
            "start_time": output_item["start_time"],
            "end_time": output_item["end_time"]
        }

    def generate_multilevel_explanation(self, result, impact, is_aligned):
        explanations = {}
        for level in self.explanation_levels:
            explanations[level] = self._generate_explanation_by_level(result, impact, is_aligned, level)
        return explanations

    def _generate_explanation_by_level(self, result, impact, is_aligned, level):
        if level == "simple":
            return self._simplify_explanation(self.generate(result, impact, is_aligned))
        elif level == "detailed":
            return self.generate(result, impact, is_aligned)
        elif level == "technical":
            return self._elaborate_explanation(self.generate(result, impact, is_aligned))

    def _format_result(self, result: Dict[str, Any]) -> str:
        return ", ".join(f"{k}: {v}" for k, v in result.items())

    def _simplify_explanation(self, explanation):
        # This is a placeholder for a more sophisticated simplification algorithm
        simplified = explanation.split('\n')[:3]  # Keep only the first three lines
        return '\n'.join(simplified) + "\n... (simplified for brevity)"

    def _elaborate_explanation(self, explanation):
        # This is a placeholder for a more sophisticated elaboration algorithm
        elaborated = explanation + "\nAdditional technical details:\n"
        elaborated += "- Implementation specifics: [Placeholder]\n"
        elaborated += "- Performance metrics: [Placeholder]\n"
        elaborated += "- Error analysis: [Placeholder]\n"
        return elaborated

    def generate_step_by_step_explanation(self, process, steps):
        try:
            explanation = f"Step-by-step explanation of the {process} process:\n"
            for i, step in enumerate(steps, 1):
                explanation += f"{i}. {step}\n"
            self.logger.info(f"Generated step-by-step explanation for {process}")
            return explanation
        except Exception as e:
            self.error_handler.handle_error(e, f"Error generating step-by-step explanation for {process}")
            return "Unable to generate step-by-step explanation."