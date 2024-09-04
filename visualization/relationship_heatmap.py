import plotly.graph_objs as go
import numpy as np
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class RelationshipHeatmap:
    def __init__(self, graph_structure):
        self.graph_structure = graph_structure
        self.logger = Logger("RelationshipHeatmap")
        self.error_handler = ErrorHandler()

    def create_heatmap(self, max_nodes=50):
        try:
            G = self.graph_structure.to_networkx()
            nodes = list(G.nodes())[:max_nodes]
            n = len(nodes)
            
            adjacency_matrix = np.zeros((n, n))
            for i, node1 in enumerate(nodes):
                for j, node2 in enumerate(nodes):
                    if G.has_edge(node1, node2):
                        adjacency_matrix[i][j] = 1

            heatmap = go.Heatmap(
                z=adjacency_matrix,
                x=nodes,
                y=nodes,
                colorscale='Viridis'
            )

            layout = go.Layout(
                title='Relationship Heatmap',
                xaxis=dict(title='Nodes'),
                yaxis=dict(title='Nodes')
            )

            fig = go.Figure(data=[heatmap], layout=layout)
            return fig
        except Exception as e:
            self.error_handler.handle_error(e, "Error creating relationship heatmap")
            return None

    def save_heatmap(self, filename='relationship_heatmap.html'):
        fig = self.create_heatmap()
        if fig:
            fig.write_html(filename)
            self.logger.info(f"Relationship heatmap saved to {filename}")
        else:
            self.logger.error("Failed to save relationship heatmap")