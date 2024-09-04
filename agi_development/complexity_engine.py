import networkx as nx
import numpy as np
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class ComplexityEngine:
    def __init__(self):
        self.logger = Logger("ComplexityEngine")
        self.error_handler = ErrorHandler()
        self.graph = nx.Graph()

    def add_node(self, node_id, attributes=None):
        try:
            self.graph.add_node(node_id, **(attributes or {}))
            self.logger.info(f"Added node: {node_id}")
        except Exception as e:
            self.error_handler.handle_error(e, f"Error adding node: {node_id}")

    def add_edge(self, node1, node2, weight=1):
        try:
            self.graph.add_edge(node1, node2, weight=weight)
            self.logger.info(f"Added edge: {node1} - {node2}")
        except Exception as e:
            self.error_handler.handle_error(e, f"Error adding edge: {node1} - {node2}")

    def calculate_complexity(self):
        try:
            num_nodes = self.graph.number_of_nodes()
            num_edges = self.graph.number_of_edges()
            avg_degree = 2 * num_edges / num_nodes if num_nodes > 0 else 0
            clustering_coefficient = nx.average_clustering(self.graph)
            
            complexity = (avg_degree * clustering_coefficient) / (num_nodes ** 0.5)
            return complexity
        except Exception as e:
            self.error_handler.handle_error(e, "Error calculating complexity")
            return None

    def identify_hubs(self, threshold=0.9):
        try:
            degree_centrality = nx.degree_centrality(self.graph)
            sorted_nodes = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)
            top_10_percent = int(len(sorted_nodes) * 0.1)
            hubs = [node for node, centrality in sorted_nodes[:top_10_percent] if centrality > threshold]
            return hubs
        except Exception as e:
            self.error_handler.handle_error(e, "Error identifying hubs")
            return []

    def simulate_information_flow(self, start_node, num_steps):
        try:
            current_nodes = [start_node]
            visited = set()
            flow_path = []

            for _ in range(num_steps):
                next_nodes = []
                for node in current_nodes:
                    neighbors = list(self.graph.neighbors(node))
                    if neighbors:
                        next_node = np.random.choice(neighbors)
                        if next_node not in visited:
                            next_nodes.append(next_node)
                            visited.add(next_node)
                            flow_path.append((node, next_node))
                
                current_nodes = next_nodes
                if not current_nodes:
                    break

            return flow_path
        except Exception as e:
            self.error_handler.handle_error(e, "Error simulating information flow")
            return []

    def detect_emergent_patterns(self):
        try:
            communities = list(nx.community.greedy_modularity_communities(self.graph))
            patterns = []
            for i, community in enumerate(communities):
                subgraph = self.graph.subgraph(community)
                pattern = {
                    'community_id': i,
                    'size': len(community),
                    'density': nx.density(subgraph),
                    'avg_clustering': nx.average_clustering(subgraph)
                }
                patterns.append(pattern)
            return patterns
        except Exception as e:
            self.error_handler.handle_error(e, "Error detecting emergent patterns")
            return []