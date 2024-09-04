import json

class RelationshipExtractor:
    def extract(self, scenario, action, outcome):
        relationships = []
        
        action_type = action.get('type', 'unknown_action') if isinstance(action, dict) else 'unknown_action'
        
        relationships.append({
            'start': 'scenario',
            'end': action_type,
            'type': 'LEADS_TO',
            'properties': self._sanitize_dict({})
        })
        
        relationships.append({
            'start': action_type,
            'end': 'outcome',
            'type': 'RESULTS_IN',
            'properties': self._sanitize_dict({})
        })
        
        return relationships

    def _sanitize_properties(self, value):
        if isinstance(value, (str, int, float, bool)):
            return value
        elif isinstance(value, (list, dict)):
            return json.dumps(value)
        else:
            return str(value)

    def _sanitize_dict(self, d):
        return {k: self._sanitize_properties(v) for k, v in d.items()}