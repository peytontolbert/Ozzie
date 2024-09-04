from utils.logger import Logger
from utils.error_handler import ErrorHandler

class ContextAnalyzer:
    def __init__(self, nl_parser):
        self.nl_parser = nl_parser
        self.logger = Logger("ContextAnalyzer")
        self.error_handler = ErrorHandler()
        self.context = {}

    def analyze_context(self, text, additional_context=None):
        try:
            parsed_text = self.nl_parser.parse(text)
            if not parsed_text:
                return None

            self.context = {
                'entities': parsed_text['entities'],
                'keywords': self.nl_parser.extract_keywords(text),
                'sentiment': self.nl_parser.analyze_sentiment(text)
            }

            if additional_context:
                self.context.update(additional_context)

            return self.context
        except Exception as e:
            self.error_handler.handle_error(e, "Error analyzing context")
            return None

    def get_relevant_context(self, query):
        try:
            query_keywords = set(self.nl_parser.extract_keywords(query))
            relevant_context = {}

            for key, value in self.context.items():
                if isinstance(value, list):
                    relevant_items = [item for item in value if any(keyword in str(item).lower() for keyword in query_keywords)]
                    if relevant_items:
                        relevant_context[key] = relevant_items
                elif isinstance(value, dict):
                    relevant_items = {k: v for k, v in value.items() if any(keyword in str(k).lower() or keyword in str(v).lower() for keyword in query_keywords)}
                    if relevant_items:
                        relevant_context[key] = relevant_items
                elif any(keyword in str(value).lower() for keyword in query_keywords):
                    relevant_context[key] = value

            return relevant_context
        except Exception as e:
            self.error_handler.handle_error(e, "Error getting relevant context")
            return None

    def update_context(self, new_context):
        try:
            self.context.update(new_context)
            self.logger.info("Context updated successfully")
        except Exception as e:
            self.error_handler.handle_error(e, "Error updating context")