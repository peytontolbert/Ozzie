import networkx as nx
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class KnowledgeFlowAnalyzer:
    def __init__(self, graph_structure):
        self.graph = graph_structure
        self.logger = Logger("KnowledgeFlowAnalyzer")
        self.error_handler = ErrorHandler()

    def calculate_information_flow(self, source, target):
        try:
            G = self.graph.to_networkx()
            max_flow_value, flow_dict = nx.maximum_flow(G, source, target)
            return max_flow_value, flow_dict
        except Exception as e:
            self.error_handler.handle_error(e, f"Error calculating information flow from {source} to {target}")
            return None, None

    def identify_bottlenecks(self):
        try:
            G = self.graph.to_networkx()
            bottleneck_centrality = nx.betweenness_centrality(G)
            sorted_bottlenecks = sorted(bottleneck_centrality.items(), key=lambda x: x[1], reverse=True)
            return sorted_bottlenecks[:10]  # Return top 10 bottlenecks
        except Exception as e:
            self.error_handler.handle_error(e, "Error identifying bottlenecks")
            return []

    def calculate_knowledge_diffusion(self, start_node, time_steps):
        try:
            G = self.graph.to_networkx()
            diffusion = {node: 0 for node in G.nodes()}
            diffusion[start_node] = 1
            
            for _ in range(time_steps):
                new_diffusion = diffusion.copy()
                for node in G.nodes():
                    neighbors = list(G.neighbors(node))
                    for neighbor in neighbors:
                        new_diffusion[neighbor] += diffusion[node] / len(neighbors)
                diffusion = new_diffusion
            
            return diffusion
        except Exception as e:
            self.error_handler.handle_error(e, f"Error calculating knowledge diffusion from {start_node}")
            return {}

    def identify_knowledge_hubs(self, top_n=5):
        try:
            G = self.graph.to_networkx()
            degree_centrality = nx.degree_centrality(G)
            sorted_hubs = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)
            return sorted_hubs[:top_n]
        except Exception as e:
            self.error_handler.handle_error(e, "Error identifying knowledge hubs")
            return []