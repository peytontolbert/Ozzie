import importlib
import os
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class PluginManager:
    def __init__(self, plugin_directory):
        self.plugin_directory = plugin_directory
        self.plugins = {}
        self.logger = Logger("PluginManager")
        self.error_handler = ErrorHandler()

    def load_plugins(self):
        try:
            for filename in os.listdir(self.plugin_directory):
                if filename.endswith('.py') and not filename.startswith('__'):
                    module_name = filename[:-3]
                    module_path = f"{self.plugin_directory}.{module_name}"
                    module = importlib.import_module(module_path)
                    
                    if hasattr(module, 'plugin_main'):
                        self.plugins[module_name] = module.plugin_main
                        self.logger.info(f"Loaded plugin: {module_name}")
                    else:
                        self.logger.warning(f"No plugin_main function found in {module_name}")
        except Exception as e:
            self.error_handler.handle_error(e, "Error loading plugins")

    def execute_plugin(self, plugin_name, *args, **kwargs):
        if plugin_name not in self.plugins:
            self.logger.error(f"Plugin {plugin_name} not found")
            return None

        try:
            return self.plugins[plugin_name](*args, **kwargs)
        except Exception as e:
            self.error_handler.handle_error(e, f"Error executing plugin {plugin_name}")
            return None

    def list_plugins(self):
        return list(self.plugins.keys())

    def get_plugin_info(self, plugin_name):
        if plugin_name not in self.plugins:
            self.logger.error(f"Plugin {plugin_name} not found")
            return None

        try:
            module = importlib.import_module(f"{self.plugin_directory}.{plugin_name}")
            return getattr(module, 'plugin_info', "No information available")
        except Exception as e:
            self.error_handler.handle_error(e, f"Error getting info for plugin {plugin_name}")
            return None