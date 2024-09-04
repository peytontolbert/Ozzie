import asyncio
from utils.logger import Logger
from utils.error_handler import ErrorHandler
from .knowledge_graph_updater import KnowledgeGraphUpdater
from .scenario_processor import ScenarioProcessor
from .action_selector import ActionSelector

class AutonomousLoop:
    def __init__(self, agi_components, virtual_environment):
        self.agi_components = agi_components
        self.virtual_environment = virtual_environment
        self.logger = Logger("AutonomousLoop")
        self.error_handler = ErrorHandler()
        self.knowledge_graph_updater = KnowledgeGraphUpdater(agi_components["knowledge_graph"], self.logger, self.error_handler)
        self.scenario_processor = ScenarioProcessor(agi_components, self.logger, self.error_handler)
        self.action_selector = ActionSelector(self.logger, self.error_handler)

    async def run(self):
        self.logger.info("Starting autonomous loop")
        while True:
            try:
                scenario = await self.agi_components['experience_engine'].generate_scenario()
                if not scenario:
                    self.logger.warning("Failed to generate scenario. Skipping this cycle.")
                    continue

                action = await self.scenario_processor.process(scenario)
                outcome = await self.agi_components['experience_engine'].evaluate_outcome(action, scenario)

                await self.knowledge_graph_updater.update(scenario, action, outcome)

                self.logger.info(f"Cycle completed. Action: {action}, Outcome: {outcome}")

                await self.virtual_environment.process_autonomous_cycle(
                    {"scenario": scenario, "action": action, "outcome": outcome},
                    "Autonomous cycle completed successfully."
                )

                await asyncio.sleep(1)
            except Exception as e:
                self.error_handler.handle_error(e, "Error in autonomous loop")
                await asyncio.sleep(5)