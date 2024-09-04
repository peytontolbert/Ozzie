import networkx as nx
import community
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class CommunityDetector:
    def __init__(self, graph_structure):
        self.graph = graph_structure
        self.logger = Logger("CommunityDetector")
        self.error_handler = ErrorHandler()

    def detect_communities_louvain(self):
        try:
            G = self.graph.to_networkx()
            partition = community.best_partition(G)
            return partition
        except Exception as e:
            self.error_handler.handle_error(e, "Error detecting communities using Louvain method")
            return {}

    def detect_communities_label_propagation(self):
        try:
            G = self.graph.to_networkx()
            return nx.algorithms.community.label_propagation_communities(G)
        except Exception as e:
            self.error_handler.handle_error(e, "Error detecting communities using Label Propagation")
            return []

    def calculate_modularity(self, partition):
        try:
            G = self.graph.to_networkx()
            return community.modularity(partition, G)
        except Exception as e:
            self.error_handler.handle_error(e, "Error calculating modularity")
            return None

    def get_community_sizes(self, partition):
        try:
            community_sizes = {}
            for node, community_id in partition.items():
                if community_id not in community_sizes:
                    community_sizes[community_id] = 0
                community_sizes[community_id] += 1
            return community_sizes
        except Exception as e:
            self.error_handler.handle_error(e, "Error getting community sizes")
            return {}

    def get_nodes_in_community(self, partition, community_id):
        try:
            return [node for node, comm_id in partition.items() if comm_id == community_id]
        except Exception as e:
            self.error_handler.handle_error(e, f"Error getting nodes in community {community_id}")
            return []