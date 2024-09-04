from chat_with_ollama import ChatGPT
from utils.logger import Logger
from utils.error_handler import ErrorHandler
import json

class ExperienceEngine:
    def __init__(self):
        self.chat_gpt = ChatGPT()
        self.last_scenario = None
        self.last_action = None
        self.last_outcome = None
        self.logger = Logger("ExperienceEngine")
        self.error_handler = ErrorHandler()

    def initialize(self):
        # Add any initialization logic here if needed
        self.logger.info("ExperienceEngine initialized")

    async def generate_scenario(self):
        try:
            system_prompt = "You are an AI that generates challenging scenarios for AI agents. Generate a scenario in JSON format with 'description' and 'difficulty' fields."
            prompt = "Create a challenging scenario for an AI agent to solve."
            
            response = await self.chat_gpt.chat_with_ollama(system_prompt, prompt)
            self.last_scenario = self._parse_json_response(response)
            return self.last_scenario
        except Exception as e:
            self.error_handler.handle_error(e, "Error generating scenario")
            return None

    async def evaluate_outcome(self, action, scenario):
        try:
            self.last_action = action
            system_prompt = "You are an AI that evaluates outcomes of actions in given scenarios. Evaluate the following and respond in JSON format with 'outcome' and 'score' fields."
            prompt = f"Scenario: {scenario}\nAction: {action}\nEvaluate the outcome:"
            
            response = await self.chat_gpt.chat_with_ollama(system_prompt, prompt)
            self.last_outcome = self._parse_json_response(response)
            return self.last_outcome
        except Exception as e:
            self.error_handler.handle_error(e, "Error evaluating outcome")
            return None

    def _parse_json_response(self, response):
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            self.logger.warning("Failed to parse JSON response, returning raw text")
            return {"raw_text": response}