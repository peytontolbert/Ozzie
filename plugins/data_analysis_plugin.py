import pandas as pd
import matplotlib.pyplot as plt
from plugin_core.plugin_interface import PluginInterface, plugin_info

class DataAnalysisPlugin(PluginInterface):
    def execute(self, data, analysis_type):
        if analysis_type == "summary":
            return self.generate_summary(data)
        elif analysis_type == "visualization":
            return self.generate_visualization(data)
        else:
            return f"Unsupported analysis type: {analysis_type}"

    def generate_summary(self, data):
        df = pd.DataFrame(data)
        return df.describe().to_dict()

    def generate_visualization(self, data):
        df = pd.DataFrame(data)
        plt.figure(figsize=(10, 6))
        df.plot(kind='bar')
        plt.title('Data Visualization')
        plt.xlabel('Index')
        plt.ylabel('Value')
        plt.tight_layout()
        plt.savefig('data_visualization.png')
        return "Visualization saved as data_visualization.png"

    def get_info(self):
        return plugin_info

def plugin_main(*args, **kwargs):
    return DataAnalysisPlugin()

plugin_info = {
    "name": "Data Analysis Plugin",
    "version": "1.0",
    "description": "Performs basic data analysis and visualization",
    "author": "Your Name",
}