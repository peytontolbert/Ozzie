import time
from datetime import datetime

class KnowledgeEvolution:
    def __init__(self, web_structure, data_store):
        self.web_structure = web_structure
        self.data_store = data_store

    def track_concept_changes(self, concept_id, interval=86400):  # Default interval is 1 day
        while True:
            initial_state = self.web_structure.get_concept(concept_id)
            time.sleep(interval)
            current_state = self.web_structure.get_concept(concept_id)
            changes = self.compare_states(initial_state, current_state)
            if changes:
                self.record_changes(concept_id, changes)

    def compare_states(self, initial_state, current_state):
        changes = {}
        for key in set(initial_state.keys()) | set(current_state.keys()):
            if key not in initial_state:
                changes[key] = {'type': 'added', 'value': current_state[key]}
            elif key not in current_state:
                changes[key] = {'type': 'removed', 'value': initial_state[key]}
            elif initial_state[key] != current_state[key]:
                changes[key] = {'type': 'modified', 'old_value': initial_state[key], 'new_value': current_state[key]}
        return changes

    def record_changes(self, concept_id, changes):
        timestamp = datetime.now().isoformat()
        change_record = {
            'concept_id': concept_id,
            'timestamp': timestamp,
            'changes': changes
        }
        self.data_store.save(f"change_record_{concept_id}_{timestamp}", change_record)

    def analyze_evolution_trends(self, concept_id, time_range):
        change_records = self.get_change_records(concept_id, time_range)
        trends = self.identify_trends(change_records)
        return trends

    def get_change_records(self, concept_id, time_range):
        # This is a simplified version. In a real system, you'd query the data store more efficiently.
        all_records = [self.data_store.load(key) for key in self.data_store.list_keys() if key.startswith(f"change_record_{concept_id}_")]
        return [record for record in all_records if self.is_in_time_range(record['timestamp'], time_range)]

    def is_in_time_range(self, timestamp, time_range):
        record_time = datetime.fromisoformat(timestamp)
        return time_range[0] <= record_time <= time_range[1]

    def identify_trends(self, change_records):
        property_changes = {}
        for record in change_records:
            for key, change in record['changes'].items():
                if key not in property_changes:
                    property_changes[key] = []
                property_changes[key].append(change)

        trends = {}
        for key, changes in property_changes.items():
            trend = self.analyze_property_trend(changes)
            if trend:
                trends[key] = trend

        return trends

    def analyze_property_trend(self, changes):
        if len(changes) < 2:
            return None

        if all(change['type'] == 'modified' for change in changes):
            values = [change['new_value'] for change in changes]
            if all(isinstance(v, (int, float)) for v in values):
                return self.analyze_numeric_trend(values)
            elif all(isinstance(v, str) for v in values):
                return self.analyze_string_trend(values)

        return self.analyze_general_trend(changes)

    def analyze_numeric_trend(self, values):
        diffs = [values[i+1] - values[i] for i in range(len(values)-1)]
        avg_diff = sum(diffs) / len(diffs)
        if avg_diff > 0:
            return "Increasing"
        elif avg_diff < 0:
            return "Decreasing"
        else:
            return "Stable"

    def analyze_string_trend(self, values):
        unique_values = set(values)
        if len(unique_values) == 1:
            return "Constant"
        elif len(unique_values) == len(values):
            return "Highly variable"
        else:
            return "Variable with some repetition"

    def analyze_general_trend(self, changes):
        change_types = [change['type'] for change in changes]
        if all(t == 'added' for t in change_types):
            return "Expanding"
        elif all(t == 'removed' for t in change_types):
            return "Shrinking"
        else:
            return "Mixed changes"