import logging

class ErrorHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def handle_error(self, error, context):
        self.logger.error(f"Error: {str(error)} | Context: {context}")
        # Implement additional error handling logic here, such as:
        # - Sending error notifications
        # - Attempting to recover from the error
        # - Logging additional debug information

    def raise_error(self, error_type, message, context=None):
        self.handle_error(f"{error_type}: {message}", context)
        raise error_type(message)