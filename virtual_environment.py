from agent_manager import AgentManager
from experience_engine import ExperienceEngine
from main_menu import MainMenu
from utils.logger import Logger  # Add this import
import asyncio

class VirtualEnvironment:
    def __init__(self, experience_engine):
        self.experience_engine = experience_engine
        self.main_menu = MainMenu()
        self.agent_manager = AgentManager()
        self.current_agent = None
        self.event_queue = asyncio.Queue()
        self.logger = Logger("VirtualEnvironment")

    def initialize(self):
        self.main_menu.initialize()
        self.agent_manager.initialize()
        if hasattr(self.experience_engine, 'initialize'):
            self.experience_engine.initialize()
        else:
            print("ExperienceEngine does not have an initialize method. Skipping initialization.")

    def run(self):
        # Main application loop
        while True:
            selection = self.main_menu.display()
            if selection == "exit":
                break
            self.handle_selection(selection)

    def handle_selection(self, selection):
        if selection == "create_agent":
            name = input("Enter agent name: ")
            self.current_agent = self.agent_manager.create_agent(name)
            print(f"Agent {name} created.")
        elif selection == "load_agent":
            name = input("Enter agent name to load: ")
            self.current_agent = self.agent_manager.load_agent(name)
            print(f"Agent {name} loaded.")
        elif selection == "run_scenario":
            if self.current_agent:
                self.run_scenario()
            else:
                print("Please create or load an agent first.")

    def run_scenario(self):
        scenario = self.experience_engine.generate_scenario()
        print(f"Scenario: {scenario}")
        action = input("Enter agent's action: ")
        outcome = self.experience_engine.evaluate_outcome(action, scenario)
        print(f"Outcome: {outcome}")
        self.current_agent.learn({"scenario": scenario, "action": action, "outcome": outcome})

    async def publish_event(self, event):
        await self.event_queue.put(event)
        self.logger.info(f"Event published: {event}")

    async def process_events(self):
        while True:
            event = await self.event_queue.get()
            # Process the event (you can implement the logic here)
            self.logger.info(f"Processing event: {event}")
            # Simulate event processing
            await asyncio.sleep(0.1)
            self.event_queue.task_done()

    async def process_cycle(self, result, explanation):
        # Process the result of an autonomous cycle
        print(f"Processing cycle result: {result}")
        print(f"Explanation: {explanation}")
        if self.current_agent:
            self.current_agent.learn({"result": result, "explanation": explanation})

    async def process_autonomous_cycle(self, result, explanation):
        print(f"Processing autonomous cycle result: {result}")
        print(f"Explanation: {explanation}")
        if self.current_agent:
            self.current_agent.learn({"result": result, "explanation": explanation})
        # Update the experience engine with the latest scenario, action, and outcome
        if hasattr(self.experience_engine, 'last_scenario'):
            self.experience_engine.last_scenario = result.get('scenario')
        if hasattr(self.experience_engine, 'last_action'):
            self.experience_engine.last_action = result.get('action')
        if hasattr(self.experience_engine, 'last_outcome'):
            self.experience_engine.last_outcome = result.get('outcome')
