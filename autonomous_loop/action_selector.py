import random

class ActionSelector:
    def __init__(self, logger, error_handler):
        self.logger = logger
        self.error_handler = error_handler

    async def select(self, scenario, reasoning_result, workflow_result):
        try:
            self.logger.debug(f"Selecting action for scenario: {scenario}")
            self.logger.debug(f"Reasoning result: {reasoning_result}")
            self.logger.debug(f"Workflow result: {workflow_result}")

            environment_state = scenario.get('environment_state', {})
            entities = environment_state.get('entities', {})

            action_options = self._generate_action_options(entities)

            if workflow_result:
                for result in workflow_result:
                    if isinstance(result, dict) and 'action_suggestion' in result:
                        action_options.append(result['action_suggestion'])

            if not action_options:
                self.logger.warning("No valid actions found. Returning wait action.")
                return {"type": "wait"}

            selected_action = random.choice(action_options)
            self.logger.debug(f"Selected action from options: {selected_action}")
            return selected_action
        except Exception as e:
            self.error_handler.handle_error(e, f"Error selecting action: {str(e)}")
            return {"type": "default_action"}

    def _generate_action_options(self, entities):
        action_options = []
        for entity_id, entity in entities.items():
            if isinstance(entity, dict) and entity.get('properties', {}).get('status') == 'idle':
                nearby_entities = self._get_nearby_entities(entity, entities)
                for nearby_entity_id in nearby_entities:
                    action_options.append({
                        "type": "interact",
                        "entity_id": entity_id,
                        "target_id": nearby_entity_id
                    })
                action_options.append({
                    "type": "move",
                    "entity_id": entity_id,
                    "direction": self._generate_random_direction()
                })
        return action_options

    def _get_nearby_entities(self, entity, entities, range=10.0):
        # Implementation of _get_nearby_entities method
        pass

    def _generate_random_direction(self):
        # Implementation of _generate_random_direction method
        pass