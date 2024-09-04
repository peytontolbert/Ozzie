import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import networkx as nx
import plotly.graph_objs as go
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class InteractiveExplorer:
    def __init__(self, graph_structure):
        self.graph_structure = graph_structure
        self.logger = Logger("InteractiveExplorer")
        self.error_handler = ErrorHandler()
        self.app = dash.Dash(__name__)
        self.setup_layout()

    def setup_layout(self):
        self.app.layout = html.Div([
            html.H1("Interactive Knowledge Graph Explorer"),
            dcc.Dropdown(
                id='node-dropdown',
                options=[{'label': node, 'value': node} for node in self.graph_structure.get_all_nodes()],
                value=None,
                placeholder="Select a node"
            ),
            dcc.Graph(id='graph-visualization')
        ])

        @self.app.callback(
            Output('graph-visualization', 'figure'),
            [Input('node-dropdown', 'value')]
        )
        def update_graph(selected_node):
            return self.create_visualization(selected_node)

    def create_visualization(self, center_node=None):
        try:
            G = self.graph_structure.to_networkx()
            if center_node:
                neighbors = list(G.neighbors(center_node))
                G = G.subgraph([center_node] + neighbors)

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
                    colorscale='YlGnBu',
                    size=10,
                    colorbar=dict(thickness=15, title='Node Connections', xanchor='left', titleside='right')
                )
            )

            for node in G.nodes():
                x, y = pos[node]
                node_trace['x'] += (x,)
                node_trace['y'] += (y,)
                node_info = f"Node: {node}<br>Degree: {G.degree(node)}"
                node_trace['text'] += (node_info,)

            fig = go.Figure(data=[edge_trace, node_trace],
                            layout=go.Layout(
                                title='Interactive Knowledge Graph',
                                titlefont=dict(size=16),
                                showlegend=False,
                                hovermode='closest',
                                margin=dict(b=20,l=5,r=5,t=40),
                                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                            ))

            return fig
        except Exception as e:
            self.error_handler.handle_error(e, "Error creating interactive visualization")
            return go.Figure()

    def run(self, debug=False, port=8050):
        self.app.run_server(debug=debug, port=port)