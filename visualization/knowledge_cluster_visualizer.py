import networkx as nx
import community
import plotly.graph_objs as go
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class KnowledgeClusterVisualizer:
    def __init__(self, graph_structure):
        self.graph_structure = graph_structure
        self.logger = Logger("KnowledgeClusterVisualizer")
        self.error_handler = ErrorHandler()

    def detect_clusters(self):
        try:
            G = self.graph_structure.to_networkx()
            partition = community.best_partition(G)
            return partition
        except Exception as e:
            self.error_handler.handle_error(e, "Error detecting clusters")
            return None

    def create_cluster_visualization(self):
        try:
            G = self.graph_structure.to_networkx()
            partition = self.detect_clusters()
            
            if not partition:
                return None

            pos = nx.spring_layout(G)
            
            edge_trace = go.Scatter(
                x=[], y=[], line=dict(width=0.5, color='#888'), hoverinfo='none', mode='lines')
            for edge in G.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_trace['x'] += (x0, x1, None)
                edge_trace['y'] += (y0, y1, None)

            node_trace = go.Scatter(
                x=[], y=[], text=[], mode='markers', hoverinfo='text',
                marker=dict(
                    showscale=True,
                    colorscale='Viridis',
                    size=10,
                    colorbar=dict(thickness=15, title='Cluster', xanchor='left', titleside='right')
                )
            )

            for node in G.nodes():
                x, y = pos[node]
                node_trace['x'] += (x,)
                node_trace['y'] += (y,)
                node_info = f"Node: {node}<br>Cluster: {partition[node]}"
                node_trace['text'] += (node_info,)
                node_trace['marker']['color'] += (partition[node],)

            fig = go.Figure(data=[edge_trace, node_trace],
                            layout=go.Layout(
                                title='Knowledge Clusters',
                                titlefont=dict(size=16),
                                showlegend=False,
                                hovermode='closest',
                                margin=dict(b=20,l=5,r=5,t=40),
                                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                            ))

            return fig
        except Exception as e:
            self.error_handler.handle_error(e, "Error creating cluster visualization")
            return None

    def save_cluster_visualization(self, filename='knowledge_clusters.html'):
        fig = self.create_cluster_visualization()
        if fig:
            fig.write_html(filename)
            self.logger.info(f"Knowledge cluster visualization saved to {filename}")
        else:
            self.logger.error("Failed to save knowledge cluster visualization")