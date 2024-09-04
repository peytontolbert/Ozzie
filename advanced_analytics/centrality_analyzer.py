import networkx as nx
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class CentralityAnalyzer:
    def __init__(self, graph_structure):
        self.graph = graph_structure
        self.logger = Logger("CentralityAnalyzer")
        self.error_handler = ErrorHandler()

    def calculate_degree_centrality(self):
        try:
            G = self.graph.to_networkx()
            return nx.degree_centrality(G)
        except Exception as e:
            self.error_handler.handle_error(e, "Error calculating degree centrality")
            return {}

    def calculate_betweenness_centrality(self):
        try:
            G = self.graph.to_networkx()
            return nx.betweenness_centrality(G)
        except Exception as e:
            self.error_handler.handle_error(e, "Error calculating betweenness centrality")
            return {}

    def calculate_closeness_centrality(self):
        try:
            G = self.graph.to_networkx()
            return nx.closeness_centrality(G)
        except Exception as e:
            self.error_handler.handle_error(e, "Error calculating closeness centrality")
            return {}

    def calculate_eigenvector_centrality(self):
        try:
            G = self.graph.to_networkx()
            return nx.eigenvector_centrality(G)
        except Exception as e:
            self.error_handler.handle_error(e, "Error calculating eigenvector centrality")
            return {}

    def get_top_central_nodes(self, centrality_measure, top_n=10):
        try:
            if centrality_measure == "degree":
                centrality = self.calculate_degree_centrality()
            elif centrality_measure == "betweenness":
                centrality = self.calculate_betweenness_centrality()
            elif centrality_measure == "closeness":
                centrality = self.calculate_closeness_centrality()
            elif centrality_measure == "eigenvector":
                centrality = self.calculate_eigenvector_centrality()
            else:
                raise ValueError(f"Unknown centrality measure: {centrality_measure}")

            sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
            return sorted_nodes[:top_n]
        except Exception as e:
            self.error_handler.handle_error(e, f"Error getting top central nodes for {centrality_measure}")
            return []