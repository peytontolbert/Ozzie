import itertools
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class FeatureCombiner:
    def __init__(self, feature_repository):
        self.feature_repository = feature_repository
        self.logger = Logger("FeatureCombiner")
        self.error_handler = ErrorHandler()

    def combine_features(self, feature_list, combination_size=2):
        try:
            combinations = list(itertools.combinations(feature_list, combination_size))
            return [self._merge_features(combo) for combo in combinations]
        except Exception as e:
            self.error_handler.handle_error(e, "Error combining features")
            return []

    def _merge_features(self, feature_combo):
        merged_feature = {
            "name": " + ".join([f["name"] for f in feature_combo]),
            "description": "Combination of " + " and ".join([f["name"] for f in feature_combo]),
            "properties": {}
        }
        for feature in feature_combo:
            merged_feature["properties"].update(feature.get("properties", {}))
        return merged_feature

    def generate_new_agent_type(self, base_agent, additional_features):
        try:
            new_agent = base_agent.copy()
            new_agent["name"] += " (Enhanced)"
            new_agent["features"] = new_agent.get("features", []) + additional_features
            new_agent["description"] += f" Enhanced with {', '.join(additional_features)}."
            return new_agent
        except Exception as e:
            self.error_handler.handle_error(e, "Error generating new agent type")
            return None

    def suggest_feature_combinations(self, domain):
        try:
            domain_features = self.feature_repository.get_features_by_domain(domain)
            combinations = self.combine_features(domain_features, 3)
            return [combo for combo in combinations if self._is_viable_combination(combo)]
        except Exception as e:
            self.error_handler.handle_error(e, f"Error suggesting feature combinations for domain: {domain}")
            return []

    def _is_viable_combination(self, feature_combo):
        # This is a placeholder for more complex viability checking logic
        return len(feature_combo["properties"]) > 2