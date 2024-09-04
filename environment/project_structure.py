import os

class ProjectStructure:
    def __init__(self, root_path):
        self.root_path = root_path

    def create_default_structure(self):
        directories = [
            'src',
            'tests',
            'docs',
            'data',
            'config',
            'logs'
        ]
        for directory in directories:
            path = os.path.join(self.root_path, directory)
            if not os.path.exists(path):
                os.makedirs(path)

    def create_directory(self, path):
        full_path = os.path.join(self.root_path, path)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
            return True
        return False

    def delete_directory(self, path):
        full_path = os.path.join(self.root_path, path)
        if os.path.exists(full_path) and os.path.isdir(full_path):
            os.rmdir(full_path)
            return True
        return False

    def get_structure(self):
        structure = {}
        for root, dirs, files in os.walk(self.root_path):
            relative_path = os.path.relpath(root, self.root_path)
            structure[relative_path] = {
                'directories': dirs,
                'files': files
            }
        return structure