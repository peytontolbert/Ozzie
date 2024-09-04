import json

class EntityExtractor:
    def extract(self, scenario, action, outcome):
        entities = []
        
        if isinstance(scenario, dict):
            for key, value in scenario.items():
                if key == 'actors':
                    for actor in value:
                        actor_properties = self._sanitize_actor(actor)
                        entities.append({'name': f"actor_{actor['id']}", 'properties': actor_properties})
                elif isinstance(value, dict):
                    properties = self._sanitize_dict(value)
                    entities.append({'name': key, 'properties': properties})
                else:
                    properties = {'value': self._sanitize_properties(value)}
                    entities.append({'name': key, 'properties': properties})
        
        if isinstance(action, dict):
            properties = self._sanitize_dict(action)
            entities.append({'name': action.get('type', 'unknown_action'), 'properties': properties})
        
        if isinstance(outcome, dict):
            properties = self._sanitize_dict(outcome)
            entities.append({'name': 'outcome', 'properties': properties})
        
        return entities

    def _sanitize_properties(self, value):
        if isinstance(value, (str, int, float, bool)):
            return value
        elif isinstance(value, (list, dict)):
            return json.dumps(value)
        else:
            return str(value)

    def _sanitize_dict(self, d):
        return {k: self._sanitize_properties(v) for k, v in d.items()}

    def _sanitize_actor(self, actor):
        return {
            'id': str(actor.get('id', '')),
            'type': str(actor.get('type', '')),
            'resources': int(actor.get('resources', 0)),
            'goals': json.dumps(actor.get('goals', []))
        }