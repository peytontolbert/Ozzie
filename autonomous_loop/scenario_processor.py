import json

class ScenarioProcessor:
    def __init__(self, agi_components, logger, error_handler):
        self.agi_components = agi_components
        self.logger = logger
        self.error_handler = error_handler

    async def process(self, scenario):
        try:
            reasoning_result = await self.agi_components['abstract_reasoning_engine'].apply_reasoning(scenario)
            self.logger.debug(f"Reasoning result: {reasoning_result}")
            
            if not reasoning_result:
                self.logger.warning("Empty reasoning result. Using default action.")
                return {"type": "default_action"}
            
            workflow = await self.agi_components['workflow_engine'].generate_workflow(json.dumps(reasoning_result))
            self.logger.debug(f"Generated workflow: {workflow}")
            
            if not workflow:
                self.logger.warning("Failed to generate workflow. Using default action.")
                return {"type": "default_action"}
            
            workflow_result = await self.agi_components['workflow_engine'].execute_workflow(workflow.name)
            self.logger.debug(f"Workflow execution result: {workflow_result}")
            
            action = await self.agi_components['action_selector'].select(scenario, reasoning_result, workflow_result)
            
            if not action or 'type' not in action:
                self.logger.warning("Invalid action selected. Using default action.")
                action = {"type": "default_action"}
            
            self.logger.info(f"Selected action: {action}")
            return action
        except Exception as e:
            self.error_handler.handle_error(e, f"Error processing scenario: {str(e)}")
            return {"type": "default_action"}