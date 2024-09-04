import json
import jsonschema
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class JSONValidator:
    def __init__(self):
        self.logger = Logger("JSONValidator")
        self.error_handler = ErrorHandler()

    def validate_json(self, json_data, schema):
        try:
            jsonschema.validate(instance=json_data, schema=schema)
            self.logger.info("JSON data is valid according to the schema")
            return True
        except jsonschema.exceptions.ValidationError as ve:
            self.error_handler.handle_error(ve, "JSON validation error")
            return False
        except jsonschema.exceptions.SchemaError as se:
            self.error_handler.handle_error(se, "JSON schema error")
            return False

    def validate_json_file(self, file_path, schema):
        try:
            with open(file_path, 'r') as file:
                json_data = json.load(file)
            return self.validate_json(json_data, schema)
        except json.JSONDecodeError as je:
            self.error_handler.handle_error(je, f"JSON decode error in file: {file_path}")
            return False
        except IOError as io_error:
            self.error_handler.handle_error(io_error, f"Error reading file: {file_path}")
            return False