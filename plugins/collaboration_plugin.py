from plugin_core.plugin_interface import PluginInterface, plugin_info

class CollaborationPlugin(PluginInterface):
    def execute(self, action, data):
        if action == "share":
            return self.share_data(data)
        elif action == "merge":
            return self.merge_data(data)
        else:
            return f"Unsupported action: {action}"

    def share_data(self, data):
        # This is a simplified example
        return f"Shared data: {data}"

    def merge_data(self, data_list):
        # This is a simplified example
        merged_data = {}
        for data in data_list:
            merged_data.update(data)
        return merged_data

    def get_info(self):
        return plugin_info

def plugin_main(*args, **kwargs):
    return CollaborationPlugin()

plugin_info = {
    "name": "Collaboration Plugin",
    "version": "1.0",
    "description": "Facilitates collaboration between agents",
    "author": "Your Name",
}