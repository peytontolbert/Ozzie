import matplotlib.pyplot as plt
import networkx as nx
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class VisualizationEngine:
    def __init__(self):
        self.logger = Logger("VisualizationEngine")
        self.error_handler = ErrorHandler()

    def visualize_graph(self, nodes, edges, title="Graph Visualization"):
        try:
            G = nx.Graph()
            G.add_nodes_from(nodes)
            G.add_edges_from(edges)

            plt.figure(figsize=(12, 8))
            nx.draw(G, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
            plt.title(title)
            plt.axis('off')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            self.error_handler.handle_error(e, "Error visualizing graph")

    def visualize_workflow(self, workflow):
        # This is a placeholder for workflow visualization
        # In a real implementation, you'd parse the workflow structure and visualize it
        try:
            steps = workflow.get_steps()
            G = nx.DiGraph()
            G.add_edges_from([(i, i+1) for i in range(len(steps)-1)])

            plt.figure(figsize=(12, 8))
            pos = nx.spring_layout(G)
            nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=700, font_size=8, font_weight='bold')
            nx.draw_networkx_labels(G, pos, {i: step.__name__ for i, step in enumerate(steps)})
            plt.title(f"Workflow: {workflow.name}")
            plt.axis('off')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            self.error_handler.handle_error(e, f"Error visualizing workflow: {workflow.name}")

    def plot_performance_metrics(self, metrics, title="Performance Metrics"):
        try:
            plt.figure(figsize=(10, 6))
            plt.bar(metrics.keys(), metrics.values())
            plt.title(title)
            plt.xlabel("Metric")
            plt.ylabel("Value")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            self.error_handler.handle_error(e, "Error plotting performance metrics")