import json
import csv
import pandas as pd
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class DataProcessor:
    def __init__(self):
        self.logger = Logger("DataProcessor")
        self.error_handler = ErrorHandler()

    def load_json(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data
        except Exception as e:
            self.error_handler.handle_error(e, f"Error loading JSON file: {file_path}")
            return None

    def save_json(self, data, file_path):
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=2)
            return True
        except Exception as e:
            self.error_handler.handle_error(e, f"Error saving JSON file: {file_path}")
            return False

    def load_csv(self, file_path):
        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                data = [row for row in reader]
            return data
        except Exception as e:
            self.error_handler.handle_error(e, f"Error loading CSV file: {file_path}")
            return None

    def save_csv(self, data, file_path, fieldnames=None):
        try:
            if not fieldnames:
                fieldnames = data[0].keys() if data else []
            with open(file_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            return True
        except Exception as e:
            self.error_handler.handle_error(e, f"Error saving CSV file: {file_path}")
            return False

    def dataframe_to_dict(self, df):
        try:
            return df.to_dict(orient='records')
        except Exception as e:
            self.error_handler.handle_error(e, "Error converting DataFrame to dict")
            return None

    def dict_to_dataframe(self, data):
        try:
            return pd.DataFrame(data)
        except Exception as e:
            self.error_handler.handle_error(e, "Error converting dict to DataFrame")
            return None

    def filter_data(self, data, condition):
        try:
            return [item for item in data if condition(item)]
        except Exception as e:
            self.error_handler.handle_error(e, "Error filtering data")
            return None

    def sort_data(self, data, key, reverse=False):
        try:
            return sorted(data, key=key, reverse=reverse)
        except Exception as e:
            self.error_handler.handle_error(e, "Error sorting data")
            return None