from utils.logger import Logger
from utils.error_handler import ErrorHandler
from chat_with_ollama import ChatGPT
import json

class ContextAnalyzer:
    def __init__(self):
        self.logger = Logger("ContextAnalyzer")
        self.error_handler = ErrorHandler()
        self.chat_gpt = ChatGPT()

    async def analyze_context(self, text):
        try:
            system_prompt = "You are an AI that analyzes the context of given text. Provide entities, key phrases, sentiment, and main topics in JSON format."
            prompt = f"Analyze the context of the following text:\n\n{text}"
            
            response = await self.chat_gpt.chat_with_ollama(system_prompt, prompt)
            return self._parse_json_response(response)
        except Exception as e:
            self.error_handler.handle_error(e, "Error analyzing context")
            return None

    async def compare_contexts(self, context1, context2):
        try:
            system_prompt = "You are an AI that compares two contexts and determines their similarity. Respond in JSON format with a 'similarity_score' and 'explanation' fields."
            prompt = f"Compare the following contexts and determine their similarity:\nContext 1: {context1}\nContext 2: {context2}"
            
            response = await self.chat_gpt.chat_with_ollama(system_prompt, prompt)
            return self._parse_json_response(response)
        except Exception as e:
            self.error_handler.handle_error(e, "Error comparing contexts")
            return None

    def _parse_json_response(self, response):
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            self.logger.warning("Failed to parse JSON response, returning raw text")
            return {"raw_text": response}

    def get_relevant_context(self, query, context):
        try:
            query_keywords = set(self.extract_keywords(query))
            relevant_context = {}

            for key, value in context.items():
                if isinstance(value, (list, dict)):
                    relevant_items = self._filter_relevant_items(value, query_keywords)
                    if relevant_items:
                        relevant_context[key] = relevant_items
                elif any(keyword in str(value).lower() for keyword in query_keywords):
                    relevant_context[key] = value

            return relevant_context
        except Exception as e:
            self.error_handler.handle_error(e, "Error getting relevant context")
            return None

    def _filter_relevant_items(self, items, keywords):
        if isinstance(items, list):
            return [item for item in items if any(keyword in str(item).lower() for keyword in keywords)]
        elif isinstance(items, dict):
            return {k: v for k, v in items.items() if any(keyword in str(k).lower() or keyword in str(v).lower() for keyword in keywords)}
        return items

    def extract_keywords(self, text):
        # Simple keyword extraction (you might want to use a more sophisticated method)
        words = text.lower().split()
        return [word for word in words if len(word) > 3]

