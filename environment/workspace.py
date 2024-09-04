import os
from environment.project_structure import ProjectStructure
from environment.virtual_filesystem import VirtualFileSystem

class Workspace:
    def __init__(self, root_path):
        self.root_path = root_path
        self.project_structure = ProjectStructure(root_path)
        self.virtual_filesystem = VirtualFileSystem(root_path)

    def initialize(self):
        if not os.path.exists(self.root_path):
            os.makedirs(self.root_path)
        self.project_structure.create_default_structure()
        self.virtual_filesystem.initialize()

    def get_project_structure(self):
        return self.project_structure

    def get_virtual_filesystem(self):
        return self.virtual_filesystem

    def create_file(self, path, content):
        return self.virtual_filesystem.create_file(path, content)

    def read_file(self, path):
        return self.virtual_filesystem.read_file(path)

    def update_file(self, path, content):
        return self.virtual_filesystem.update_file(path, content)

    def delete_file(self, path):
        return self.virtual_filesystem.delete_file(path)

    def list_files(self, directory):
        return self.virtual_filesystem.list_files(directory)

    def create_directory(self, path):
        return self.virtual_filesystem.create_directory(path)

    def delete_directory(self, path):
        return self.virtual_filesystem.delete_directory(path)