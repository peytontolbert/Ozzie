import os
import shutil

class VirtualFileSystem:
    def __init__(self, root_path):
        self.root_path = root_path

    def initialize(self):
        if not os.path.exists(self.root_path):
            os.makedirs(self.root_path)

    def create_file(self, path, content):
        full_path = os.path.join(self.root_path, path)
        directory = os.path.dirname(full_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(full_path, 'w') as file:
            file.write(content)
        return True

    def read_file(self, path):
        full_path = os.path.join(self.root_path, path)
        if os.path.exists(full_path) and os.path.isfile(full_path):
            with open(full_path, 'r') as file:
                return file.read()
        return None

    def update_file(self, path, content):
        full_path = os.path.join(self.root_path, path)
        if os.path.exists(full_path) and os.path.isfile(full_path):
            with open(full_path, 'w') as file:
                file.write(content)
            return True
        return False

    def delete_file(self, path):
        full_path = os.path.join(self.root_path, path)
        if os.path.exists(full_path) and os.path.isfile(full_path):
            os.remove(full_path)
            return True
        return False

    def list_files(self, directory):
        full_path = os.path.join(self.root_path, directory)
        if os.path.exists(full_path) and os.path.isdir(full_path):
            return os.listdir(full_path)
        return []

    def create_directory(self, path):
        full_path = os.path.join(self.root_path, path)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
            return True
        return False

    def delete_directory(self, path):
        full_path = os.path.join(self.root_path, path)
        if os.path.exists(full_path) and os.path.isdir(full_path):
            shutil.rmtree(full_path)
            return True
        return False