import re
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class DataCleaner:
    def __init__(self):
        self.logger = Logger("DataCleaner")
        self.error_handler = ErrorHandler()

    def clean_text(self, text):
        try:
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            # Remove special characters
            text = re.sub(r'[^\w\s]', '', text)
            # Convert to lowercase
            text = text.lower()
            return text
        except Exception as e:
            self.error_handler.handle_error(e, "Error cleaning text")
            return text

    def remove_duplicates(self, data_list):
        try:
            return list(dict.fromkeys(data_list))
        except Exception as e:
            self.error_handler.handle_error(e, "Error removing duplicates")
            return data_list

    def normalize_dates(self, date_string):
        try:
            # This is a simple example. In a real-world scenario, you'd use a more robust date parsing library.
            date_formats = [
                r'(\d{4})-(\d{2})-(\d{2})',  # YYYY-MM-DD
                r'(\d{2})/(\d{2})/(\d{4})',  # MM/DD/YYYY
                r'(\d{2})-(\w{3})-(\d{4})'   # DD-Mon-YYYY
            ]
            for format in date_formats:
                match = re.match(format, date_string)
                if match:
                    year, month, day = match.groups()
                    return f"{year}-{month}-{day}"
            return date_string
        except Exception as e:
            self.error_handler.handle_error(e, f"Error normalizing date: {date_string}")
            return date_string

    def clean_knowledge_graph(self, knowledge_graph):
        try:
            for node in knowledge_graph.get_all_nodes():
                for key, value in node.properties.items():
                    if isinstance(value, str):
                        node.properties[key] = self.clean_text(value)
                    elif isinstance(value, list):
                        node.properties[key] = self.remove_duplicates(value)
                knowledge_graph.update_node(node)
            self.logger.info("Knowledge graph cleaned successfully")
            return True
        except Exception as e:
            self.error_handler.handle_error(e, "Error cleaning knowledge graph")
            return False