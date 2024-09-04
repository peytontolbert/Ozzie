from typing import Dict, Any, List, Union
import logging

logger = logging.getLogger(__name__)

class EthicalPrinciple:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

class ValueAlignmentVerifier:
    def __init__(self):
        self.alignment_rules = [
            lambda action: "harm" not in self._get_action_string(action).lower(),
            lambda action: "ethical" in self._get_action_string(action).lower(),
            lambda action: "beneficial" in self._get_action_string(action).lower(),
        ]

    def verify_alignment(self, action: Union[Dict[str, Any], str]) -> bool:
        action_str = self._get_action_string(action)
        alignment_score = sum(rule(action_str) for rule in self.alignment_rules)
        is_aligned = alignment_score == len(self.alignment_rules)
        return is_aligned

    def _get_action_string(self, action: Union[Dict[str, Any], str]) -> str:
        if isinstance(action, dict):
            return str(action.get('name', action.get('status', str(action))))
        return str(action)

    def add_alignment_rule(self, rule):
        if callable(rule):
            self.alignment_rules.append(rule)
        else:
            raise TypeError("Alignment rule must be a callable")

    def remove_alignment_rule(self, index):
        if 0 <= index < len(self.alignment_rules):
            return self.alignment_rules.pop(index)
        else:
            raise IndexError("Rule index out of range")

    def get_alignment_rules(self):
        return self.alignment_rules

# Usage example
if __name__ == "__main__":
    verifier = ValueAlignmentVerifier()
    test_action = {
        "name": "Recommend personalized content",
        "description": "Suggest articles based on user preferences",
        "tags": ["benefit", "personalization"]
    }
    is_aligned = verifier.verify_alignment(test_action)
    print(f"Action is aligned: {is_aligned}")
    if not is_aligned:
        print("Alignment issues:", verifier.report_alignment_issues(test_action))