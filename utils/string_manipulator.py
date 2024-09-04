import re
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class StringManipulator:
    def __init__(self):
        self.logger = Logger("StringManipulator")
        self.error_handler = ErrorHandler()

    def to_camel_case(self, string):
        try:
            words = string.split('_')
            return words[0] + ''.join(word.capitalize() for word in words[1:])
        except Exception as e:
            self.error_handler.handle_error(e, "Error converting to camel case")
            return None

    def to_snake_case(self, string):
        try:
            pattern = re.compile(r'(?<!^)(?=[A-Z])')
            return pattern.sub('_', string).lower()
        except Exception as e:
            self.error_handler.handle_error(e, "Error converting to snake case")
            return None

    def capitalize_words(self, string):
        try:
            return ' '.join(word.capitalize() for word in string.split())
        except Exception as e:
            self.error_handler.handle_error(e, "Error capitalizing words")
            return None

    def remove_special_characters(self, string):
        try:
            return re.sub(r'[^a-zA-Z0-9\s]', '', string)
        except Exception as e:
            self.error_handler.handle_error(e, "Error removing special characters")
            return None

    def truncate(self, string, length, suffix='...'):
        try:
            if len(string) <= length:
                return string
            return string[:length - len(suffix)] + suffix
        except Exception as e:
            self.error_handler.handle_error(e, "Error truncating string")
            return None

    def extract_emails(self, text):
        try:
            pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            return re.findall(pattern, text)
        except Exception as e:
            self.error_handler.handle_error(e, "Error extracting emails")
            return None

    def extract_urls(self, text):
        try:
            pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
            return re.findall(pattern, text)
        except Exception as e:
            self.error_handler.handle_error(e, "Error extracting URLs")
            return None