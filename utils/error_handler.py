from utils.logger import Logger

class ErrorHandler:
    def __init__(self):
        self.logger = Logger("ErrorHandler")

    def handle_error(self, error, context):
        error_message = f"Error: {str(error)} | Context: {context}"
        self.logger.error(error_message)
        # You can add more error handling logic here if needed

    def raise_error(self, error_type, message, context=None):
        self.handle_error(f"{error_type}: {message}", context)
        raise error_type(message)