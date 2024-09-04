from config.config_manager import ConfigManager

class EnvironmentConfig:
    def __init__(self, config_path):
        self.config_manager = ConfigManager(config_path)

    def get_workspace_root(self):
        return self.config_manager.get('workspace_root', '/default/workspace/path')

    def set_workspace_root(self, path):
        self.config_manager.set('workspace_root', path)

    def get_log_level(self):
        return self.config_manager.get('log_level', 'INFO')

    def set_log_level(self, level):
        self.config_manager.set('log_level', level)

    def get_max_agents(self):
        return self.config_manager.get('max_agents', 10)

    def set_max_agents(self, count):
        self.config_manager.set('max_agents', count)

    def get_database_url(self):
        return self.config_manager.get('database_url', 'sqlite:///default.db')

    def set_database_url(self, url):
        self.config_manager.set('database_url', url)