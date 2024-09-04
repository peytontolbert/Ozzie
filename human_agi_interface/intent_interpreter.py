from chat_with_ollama import ChatGPT
from utils.logger import Logger
from utils.error_handler import ErrorHandler
import json

class IntentInterpreter:
    def __init__(self):
        self.logger = Logger("IntentInterpreter")
        self.error_handler = ErrorHandler()
        self.chat_gpt = ChatGPT()

    async def interpret(self, input_data):
        try:
            text = input_data.get('data', '')
            system_prompt = "You are an AI assistant that interprets user intents. Extract the action, subject, object, entities, and sentiment from the following input. Respond in JSON format."
            prompt = text

            response = await self.chat_gpt.chat_with_ollama(system_prompt, prompt)
            
            # Parse the response to extract intent components
            intent = self._parse_ollama_response(response)

            self.logger.info(f"Interpreted intent: {intent}")
            return intent
        except Exception as e:
            self.error_handler.handle_error(e, "Error interpreting intent")
            return None

    def _parse_ollama_response(self, response):
        try:
            # Attempt to parse the response as JSON
            intent = json.loads(response)
            # Ensure all required keys are present
            required_keys = ['action', 'subject', 'object', 'entities', 'sentiment']
            for key in required_keys:
                if key not in intent:
                    intent[key] = None
            return intent
        except json.JSONDecodeError:
            # If JSON parsing fails, attempt to extract information using regex
            import re
            intent = {}
            patterns = {
                'action': r'"action":\s*"([^"]*)"',
                'subject': r'"subject":\s*"([^"]*)"',
                'object': r'"object":\s*"([^"]*)"',
                'sentiment': r'"sentiment":\s*"([^"]*)"'
            }
            for key, pattern in patterns.items():
                match = re.search(pattern, response)
                intent[key] = match.group(1) if match else None
            intent['entities'] = []  # Simplified entity extraction
            return intent

    def extract_keywords(self, text):
        # Implement keyword extraction logic
        # This could use NLP techniques or simply return important words
        words = text.split()
        return [word.lower() for word in words if len(word) > 3]