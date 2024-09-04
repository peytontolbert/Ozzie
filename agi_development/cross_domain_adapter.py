import numpy as np
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class CrossDomainAdapter:
    def __init__(self):
        self.logger = Logger("CrossDomainAdapter")
        self.error_handler = ErrorHandler()
        self.domain_mappings = {}

    def create_domain_mapping(self, source_domain, target_domain, mapping_function):
        try:
            self.domain_mappings[(source_domain, target_domain)] = mapping_function
            self.logger.info(f"Created mapping from {source_domain} to {target_domain}")
        except Exception as e:
            self.error_handler.handle_error(e, f"Error creating mapping from {source_domain} to {target_domain}")

    def adapt_knowledge(self, source_domain, target_domain, knowledge):
        try:
            if (source_domain, target_domain) not in self.domain_mappings:
                raise ValueError(f"No mapping found from {source_domain} to {target_domain}")
            
            mapping_function = self.domain_mappings[(source_domain, target_domain)]
            adapted_knowledge = mapping_function(knowledge)
            return adapted_knowledge
        except Exception as e:
            self.error_handler.handle_error(e, f"Error adapting knowledge from {source_domain} to {target_domain}")
            return None

    def find_analogies(self, source_domain, target_domain, source_concept):
        try:
            if (source_domain, target_domain) not in self.domain_mappings:
                raise ValueError(f"No mapping found from {source_domain} to {target_domain}")
            
            mapping_function = self.domain_mappings[(source_domain, target_domain)]
            target_concept = mapping_function(source_concept)
            return target_concept
        except Exception as e:
            self.error_handler.handle_error(e, f"Error finding analogies from {source_domain} to {target_domain}")
            return None

    def transfer_skill(self, source_domain, target_domain, skill):
        try:
            if (source_domain, target_domain) not in self.domain_mappings:
                raise ValueError(f"No mapping found from {source_domain} to {target_domain}")
            
            mapping_function = self.domain_mappings[(source_domain, target_domain)]
            adapted_skill = mapping_function(skill)
            return adapted_skill
        except Exception as e:
            self.error_handler.handle_error(e, f"Error transferring skill from {source_domain} to {target_domain}")
            return None

    def evaluate_transfer(self, source_domain, target_domain, source_performance, target_performance):
        try:
            transfer_efficiency = target_performance / source_performance
            self.logger.info(f"Transfer efficiency from {source_domain} to {target_domain}: {transfer_efficiency}")
            return transfer_efficiency
        except Exception as e:
            self.error_handler.handle_error(e, f"Error evaluating transfer from {source_domain} to {target_domain}")
            return None