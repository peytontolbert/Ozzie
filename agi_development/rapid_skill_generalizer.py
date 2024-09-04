import numpy as np
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class RapidSkillGeneralizer:
    def __init__(self):
        self.logger = Logger("RapidSkillGeneralizer")
        self.error_handler = ErrorHandler()
        self.skills = {}

    def learn_skill(self, skill_name, skill_function):
        try:
            self.skills[skill_name] = skill_function
            self.logger.info(f"Learned new skill: {skill_name}")
        except Exception as e:
            self.error_handler.handle_error(e, f"Error learning skill: {skill_name}")

    def generalize_skill(self, skill_name, new_context):
        try:
            if skill_name not in self.skills:
                raise ValueError(f"Skill not found: {skill_name}")
            
            original_skill = self.skills[skill_name]
            generalized_skill = lambda x: original_skill(self._adapt_input(x, new_context))
            return generalized_skill
        except Exception as e:
            self.error_handler.handle_error(e, f"Error generalizing skill: {skill_name}")
            return None

    def _adapt_input(self, input_data, new_context):
        # This is a placeholder for input adaptation logic
        # In a real system, this would involve more sophisticated adaptation techniques
        return input_data * new_context['adaptation_factor']

    def compose_skills(self, skill_names):
        try:
            def composed_skill(x):
                result = x
                for skill_name in skill_names:
                    if skill_name not in self.skills:
                        raise ValueError(f"Skill not found: {skill_name}")
                    result = self.skills[skill_name](result)
                return result
            return composed_skill
        except Exception as e:
            self.error_handler.handle_error(e, "Error composing skills")
            return None

    def evaluate_skill_generalization(self, skill_name, test_cases, new_context):
        try:
            if skill_name not in self.skills:
                raise ValueError(f"Skill not found: {skill_name}")
            
            original_skill = self.skills[skill_name]
            generalized_skill = self.generalize_skill(skill_name, new_context)
            
            original_results = [original_skill(case) for case in test_cases]
            generalized_results = [generalized_skill(case) for case in test_cases]
            
            similarity = np.mean([np.isclose(o, g) for o, g in zip(original_results, generalized_results)])
            self.logger.info(f"Generalization similarity for {skill_name}: {similarity}")
            return similarity
        except Exception as e:
            self.error_handler.handle_error(e, f"Error evaluating skill generalization: {skill_name}")
            return None