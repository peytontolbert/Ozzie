import networkx as nx
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class KnowledgePathFinder:
    def __init__(self, graph_structure):
        self.graph = graph_structure
        self.logger = Logger("KnowledgePathFinder")
        self.error_handler = ErrorHandler()

    def find_shortest_path(self, start_node, end_node):
        try:
            G = self.graph.to_networkx()
            path = nx.shortest_path(G, start_node, end_node)
            return path
        except nx.NetworkXNoPath:
            self.logger.info(f"No path found between {start_node} and {end_node}")
            return None
        except Exception as e:
            self.error_handler.handle_error(e, f"Error finding shortest path between {start_node} and {end_node}")
            return None

    def find_all_paths(self, start_node, end_node, cutoff=None):
        try:
            G = self.graph.to_networkx()
            paths = list(nx.all_simple_paths(G, start_node, end_node, cutoff=cutoff))
            return paths
        except Exception as e:
            self.error_handler.handle_error(e, f"Error finding all paths between {start_node} and {end_node}")
            return []

    def find_weighted_path(self, start_node, end_node, weight='weight'):
        try:
            G = self.graph.to_networkx()
            path = nx.dijkstra_path(G, start_node, end_node, weight=weight)
            return path
        except nx.NetworkXNoPath:
            self.logger.info(f"No weighted path found between {start_node} and {end_node}")
            return None
        except Exception as e:
            self.error_handler.handle_error(e, f"Error finding weighted path between {start_node} and {end_node}")
            return None

    def find_multi_source_paths(self, source_nodes, target_nodes):
        try:
            G = self.graph.to_networkx()
            paths = nx.multi_source_dijkstra_path(G, source_nodes, target_nodes)
            return paths
        except Exception as e:
            self.error_handler.handle_error(e, "Error finding multi-source paths")
            return {}

    def find_critical_path(self):
        try:
            G = self.graph.to_networkx()
            if not nx.is_directed_acyclic_graph(G):
                self.logger.warning("Graph is not a directed acyclic graph. Cannot find critical path.")
                return None
            critical_path = nx.dag_longest_path(G)
            return critical_path
        except Exception as e:
            self.error_handler.handle_error(e, "Error finding critical path")
            return None

    def calculate_path_centrality(self, path):
        try:
            G = self.graph.to_networkx()
            centrality = sum(nx.degree_centrality(G)[node] for node in path) / len(path)
            return centrality
        except Exception as e:
            self.error_handler.handle_error(e, "Error calculating path centrality")
            return 0

    def find_bottlenecks(self):
        try:
            G = self.graph.to_networkx()
            bottleneck_nodes = sorted(nx.betweenness_centrality(G).items(), key=lambda x: x[1], reverse=True)[:5]
            return bottleneck_nodes
        except Exception as e:
            self.error_handler.handle_error(e, "Error finding bottlenecks")
            return []