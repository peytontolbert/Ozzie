from utils.logger import Logger
from utils.error_handler import ErrorHandler

class EthicalEvaluator:
    def __init__(self, ethical_guidelines):
        self.ethical_guidelines = ethical_guidelines
        self.logger = Logger("EthicalEvaluator")
        self.error_handler = ErrorHandler()

    def evaluate_action(self, action, context):
        try:
            score = 0
            violations = []
            for guideline in self.ethical_guidelines:
                evaluation = guideline.evaluate(action, context)
                score += evaluation['score']
                if evaluation['violation']:
                    violations.append(evaluation['violation'])
            
            return {
                'score': score / len(self.ethical_guidelines),
                'violations': violations,
                'is_ethical': score / len(self.ethical_guidelines) >= 0.7 and not violations
            }
        except Exception as e:
            self.error_handler.handle_error(e, "Error evaluating action ethically")
            return None

    def suggest_ethical_improvements(self, action, evaluation):
        try:
            suggestions = []
            for violation in evaluation['violations']:
                suggestion = self.ethical_guidelines[violation].suggest_improvement(action)
                suggestions.append(suggestion)
            return suggestions
        except Exception as e:
            self.error_handler.handle_error(e, "Error suggesting ethical improvements")
            return None

class EthicalGuideline:
    def __init__(self, name, evaluation_function, improvement_function):
        self.name = name
        self.evaluate = evaluation_function
        self.suggest_improvement = improvement_function