from utils.logger import Logger
from utils.error_handler import ErrorHandler

class ExplanationGenerator:
    def __init__(self):
        self.logger = Logger("ExplanationGenerator")
        self.error_handler = ErrorHandler()

    def generate_explanation(self, decision, context, complexity_level='medium'):
        try:
            explanation = self._create_base_explanation(decision, context)
            explanation = self._adjust_complexity(explanation, complexity_level)
            self.logger.info(f"Generated explanation: {explanation}")
            return explanation
        except Exception as e:
            self.error_handler.handle_error(e, "Error generating explanation")
            return "Unable to generate explanation at this time."

    def _create_base_explanation(self, decision, context):
        try:
            explanation = f"The decision to {decision} was made based on the following factors:\n"
            for factor, importance in context.items():
                explanation += f"- {factor.capitalize()}: {importance}\n"
            return explanation
        except Exception as e:
            self.error_handler.handle_error(e, "Error creating base explanation")
            return "Base explanation creation failed."

    def _adjust_complexity(self, explanation, complexity_level):
        try:
            if complexity_level == 'low':
                return self._simplify_explanation(explanation)
            elif complexity_level == 'high':
                return self._elaborate_explanation(explanation)
            else:
                return explanation
        except Exception as e:
            self.error_handler.handle_error(e, "Error adjusting explanation complexity")
            return explanation

    def _simplify_explanation(self, explanation):
        # This is a placeholder for a more sophisticated simplification algorithm
        simplified = explanation.split('\n')[:3]  # Keep only the first three lines
        return '\n'.join(simplified) + "\n... (simplified for brevity)"

    def _elaborate_explanation(self, explanation):
        # This is a placeholder for a more sophisticated elaboration algorithm
        elaborated = explanation + "\nAdditional context and implications:\n"
        elaborated += "- Long-term effects: [Placeholder for long-term analysis]\n"
        elaborated += "- Alternative scenarios: [Placeholder for alternative scenarios]\n"
        elaborated += "- Confidence level: [Placeholder for confidence assessment]\n"
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