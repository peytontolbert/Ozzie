import json
from .action_selector import ActionSelector

class ScenarioProcessor:
    def __init__(self, agi_components, logger, error_handler):
        self.abstract_reasoning_engine = agi_components['abstract_reasoning_engine']
        self.workflow_engine = agi_components['workflow_engine']
        self.action_selector = ActionSelector(logger, error_handler)
        self.logger = logger
        self.error_handler = error_handler

    async def process(self, scenario):
        try:
            self.logger.debug("Applying abstract reasoning")
            reasoning_result = await self.abstract_reasoning_engine.apply_reasoning(scenario)
            self.logger.debug(f"Reasoning result: {reasoning_result}")
            
            if not reasoning_result:
                self.logger.warning("Empty reasoning result. Using default action.")
                return await self._create_default_action(scenario)
            
            self.logger.debug("Generating workflow")
            workflow = await self.workflow_engine.generate_workflow(json.dumps(reasoning_result))
            self.logger.debug(f"Generated workflow: {workflow}")
            
            if not workflow:
                self.logger.warning("Failed to generate workflow. Using default action.")
                return await self._create_default_action(scenario)
            
            self.logger.debug(f"Executing workflow: {workflow.name}")
            workflow_result = await self.workflow_engine.execute_workflow(workflow.name)
            self.logger.debug(f"Workflow execution result: {workflow_result}")
            
            self.logger.debug("Selecting action")
            action = await self.action_selector.select(scenario, reasoning_result, workflow_result)
            
            if not action or 'type' not in action:
                self.logger.warning("Invalid action selected. Using default action.")
                return await self._create_default_action(scenario)
            
            self.logger.info(f"Selected action: {action}")
            return action
        except Exception as e:
            self.error_handler.handle_error(e, f"Error processing scenario: {str(e)}")
            return await self._create_default_action(scenario)

    async def _create_default_action(self, scenario):
        return {
            "type": "default_action",
            "description": "No specific action could be determined",
            "scenario_type": scenario.get('type', 'unknown'),
            "scenario_complexity": scenario.get('complexity', 'unknown')
        }