from abc import ABC, abstractmethod

class PluginInterface(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Execute the main functionality of the plugin.
        """
        pass

    @abstractmethod
    def get_info(self):
        """
        Return information about the plugin.
        """
        pass

def plugin_main(*args, **kwargs):
    """
    This function should be implemented by each plugin to serve as the entry point.
    It should return an instance of a class that implements PluginInterface.
    """
    raise NotImplementedError("plugin_main function must be implemented by the plugin")

plugin_info = {
    "name": "Base Plugin",
    "version": "1.0",
    "description": "Base plugin interface",
    "author": "Your Name",
}