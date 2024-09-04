import traceback
from utils.logger import Logger

class ErrorHandler:
    def __init__(self):
        self.logger = Logger("ErrorHandler")

    def handle_error(self, error, context=None):
        error_message = f"Error: {str(error)}"
        if context:
            error_message += f" | Context: {context}"
        self.logger.error(error_message)
        self.logger.debug(traceback.format_exc())

    def raise_error(self, error_type, message, context=None):
        self.handle_error(f"{error_type}: {message}", context)
        raise error_type(message)