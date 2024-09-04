import networkx as nx
import plotly.graph_objs as go
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class WebVisualizer3D:
    def __init__(self, graph_structure):
        self.graph_structure = graph_structure
        self.logger = Logger("WebVisualizer3D")
        self.error_handler = ErrorHandler()

    def create_3d_visualization(self, max_nodes=100):
        try:
            G = self.graph_structure.to_networkx()
            if len(G) > max_nodes:
                G = nx.subgraph(G, list(G.nodes())[:max_nodes])

            pos = nx.spring_layout(G, dim=3)
            
            edge_trace = go.Scatter3d(
                x=[], y=[], z=[],
                line=dict(width=1, color='#888'),
                hoverinfo='none',
                mode='lines')

            for edge in G.edges():
                x0, y0, z0 = pos[edge[0]]
                x1, y1, z1 = pos[edge[1]]
                edge_trace['x'] += (x0, x1, None)
                edge_trace['y'] += (y0, y1, None)
                edge_trace['z'] += (z0, z1, None)

            node_trace = go.Scatter3d(
                x=[], y=[], z=[],
                text=[],
                mode='markers',
                hoverinfo='text',
                marker=dict(
                    showscale=True,
                    colorscale='YlGnBu',
                    size=10,
                    colorbar=dict(
                        thickness=15,
                        title='Node Connections',
                        xanchor='left',
                        titleside='right'
                    )
                )
            )

            for node in G.nodes():
                x, y, z = pos[node]
                node_trace['x'] += (x,)
                node_trace['y'] += (y,)
                node_trace['z'] += (z,)
                node_trace['text'] += (str(node),)

            fig = go.Figure(data=[edge_trace, node_trace],
                            layout=go.Layout(
                                title='3D Visualization of Knowledge Graph',
                                showlegend=False,
                                scene=dict(
                                    xaxis=dict(showticklabels=False),
                                    yaxis=dict(showticklabels=False),
                                    zaxis=dict(showticklabels=False)
                                ),
                                margin=dict(b=0, l=0, r=0, t=40),
                                hovermode='closest'
                            ))

            return fig
        except Exception as e:
            self.error_handler.handle_error(e, "Error creating 3D visualization")
            return None

    def save_visualization(self, filename='3d_visualization.html'):
        fig = self.create_3d_visualization()
        if fig:
            fig.write_html(filename)
            self.logger.info(f"3D visualization saved to {filename}")
        else:
            self.logger.error("Failed to save 3D visualization")