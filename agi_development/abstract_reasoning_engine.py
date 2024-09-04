from utils.logger import Logger
from utils.error_handler import ErrorHandler

class AbstractReasoningEngine:
    def __init__(self):
        self.logger = Logger("AbstractReasoningEngine")
        self.error_handler = ErrorHandler()
        self.knowledge_base = {}

    def add_concept(self, concept_name, properties):
        try:
            self.knowledge_base[concept_name] = properties
            self.logger.info(f"Added concept: {concept_name}")
        except Exception as e:
            self.error_handler.handle_error(e, f"Error adding concept: {concept_name}")

    def find_similarities(self, concept1, concept2):
        try:
            properties1 = set(self.knowledge_base.get(concept1, {}).keys())
            properties2 = set(self.knowledge_base.get(concept2, {}).keys())
            return properties1.intersection(properties2)
        except Exception as e:
            self.error_handler.handle_error(e, f"Error finding similarities between {concept1} and {concept2}")
            return set()

    def find_differences(self, concept1, concept2):
        try:
            properties1 = set(self.knowledge_base.get(concept1, {}).keys())
            properties2 = set(self.knowledge_base.get(concept2, {}).keys())
            return properties1.symmetric_difference(properties2)
        except Exception as e:
            self.error_handler.handle_error(e, f"Error finding differences between {concept1} and {concept2}")
            return set()

    def make_analogy(self, concept1, concept2, concept3):
        try:
            similarities = self.find_similarities(concept1, concept2)
            if not similarities:
                return None
            
            analogy = {}
            for prop in similarities:
                if prop in self.knowledge_base.get(concept3, {}):
                    analogy[prop] = self.knowledge_base[concept3][prop]
            
            return analogy
        except Exception as e:
            self.error_handler.handle_error(e, f"Error making analogy between {concept1}, {concept2}, and {concept3}")
            return None

    def abstract_common_features(self, concepts):
        try:
            common_properties = set.intersection(*[set(self.knowledge_base.get(concept, {}).keys()) for concept in concepts])
            abstraction = {prop: set() for prop in common_properties}
            
            for concept in concepts:
                for prop in common_properties:
                    abstraction[prop].add(self.knowledge_base[concept][prop])
            
            return abstraction
        except Exception as e:
            self.error_handler.handle_error(e, "Error abstracting common features")
            return {}