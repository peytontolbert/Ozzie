import json
import os
from data_storage.data_store import DataStore

class JSONFileManager(DataStore):
    def __init__(self, storage_dir):
        self.storage_dir = storage_dir
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

    def save(self, key, value):
        file_path = os.path.join(self.storage_dir, f"{key}.json")
        with open(file_path, 'w') as f:
            json.dump(value, f)

    def load(self, key):
        file_path = os.path.join(self.storage_dir, f"{key}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return None

    def delete(self, key):
        file_path = os.path.join(self.storage_dir, f"{key}.json")
        if os.path.exists(file_path):
            os.remove(file_path)

    def exists(self, key):
        file_path = os.path.join(self.storage_dir, f"{key}.json")
        return os.path.exists(file_path)