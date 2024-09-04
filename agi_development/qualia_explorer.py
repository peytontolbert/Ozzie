import random
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class QualiaExplorer:
    def __init__(self):
        self.logger = Logger("QualiaExplorer")
        self.error_handler = ErrorHandler()
        self.qualia_types = {
            'visual': ['color', 'shape', 'brightness'],
            'auditory': ['pitch', 'volume', 'timbre'],
            'tactile': ['pressure', 'temperature', 'texture'],
            'olfactory': ['intensity', 'pleasantness'],
            'gustatory': ['sweetness', 'sourness', 'bitterness', 'saltiness', 'umami'],
            'proprioceptive': ['position', 'movement'],
            'emotional': ['valence', 'arousal']
        }
        self.current_experience = {}

    def generate_qualia_experience(self):
        try:
            experience = {}
            for qualia_type, attributes in self.qualia_types.items():
                experience[qualia_type] = {attr: random.random() for attr in attributes}
            self.current_experience = experience
            self.logger.info("Generated new qualia experience")
            return experience
        except Exception as e:
            self.error_handler.handle_error(e, "Error generating qualia experience")
            return None

    def describe_experience(self):
        try:
            description = []
            for qualia_type, attributes in self.current_experience.items():
                qualia_desc = f"{qualia_type.capitalize()} experience: "
                attr_desc = [f"{attr} ({value:.2f})" for attr, value in attributes.items()]
                qualia_desc += ", ".join(attr_desc)
                description.append(qualia_desc)
            return "\n".join(description)
        except Exception as e:
            self.error_handler.handle_error(e, "Error describing experience")
            return "Unable to describe experience"

    def compare_experiences(self, experience1, experience2):
        try:
            similarities = {}
            for qualia_type in self.qualia_types:
                if qualia_type in experience1 and qualia_type in experience2:
                    attr_similarities = {}
                    for attr in self.qualia_types[qualia_type]:
                        if attr in experience1[qualia_type] and attr in experience2[qualia_type]:
                            similarity = 1 - abs(experience1[qualia_type][attr] - experience2[qualia_type][attr])
                            attr_similarities[attr] = similarity
                    similarities[qualia_type] = attr_similarities
            return similarities
        except Exception as e:
            self.error_handler.handle_error(e, "Error comparing experiences")
            return None

    def blend_experiences(self, experience1, experience2, blend_factor=0.5):
        try:
            blended_experience = {}
            for qualia_type in self.qualia_types:
                if qualia_type in experience1 and qualia_type in experience2:
                    blended_experience[qualia_type] = {}
                    for attr in self.qualia_types[qualia_type]:
                        if attr in experience1[qualia_type] and attr in experience2[qualia_type]:
                            value1 = experience1[qualia_type][attr]
                            value2 = experience2[qualia_type][attr]
                            blended_value = value1 * blend_factor + value2 * (1 - blend_factor)
                            blended_experience[qualia_type][attr] = blended_value
            return blended_experience
        except Exception as e:
            self.error_handler.handle_error(e, "Error blending experiences")
            return None

    def simulate_qualia_evolution(self, num_steps):
        try:
            evolution = []
            current_exp = self.generate_qualia_experience()
            evolution.append(current_exp)
            
            for _ in range(num_steps - 1):
                new_exp = self.generate_qualia_experience()
                current_exp = self.blend_experiences(current_exp, new_exp, 0.8)
                evolution.append(current_exp)
            
            self.logger.info(f"Simulated qualia evolution for {num_steps} steps")
            return evolution
        except Exception as e:
            self.error_handler.handle_error(e, "Error simulating qualia evolution")
            return None