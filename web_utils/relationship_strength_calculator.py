import networkx as nx
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class RelationshipStrengthCalculator:
    def __init__(self, graph_structure):
        self.graph = graph_structure
        self.logger = Logger("RelationshipStrengthCalculator")
        self.error_handler = ErrorHandler()

    def calculate_edge_strength(self, node1, node2):
        try:
            G = self.graph.to_networkx()
            if not G.has_edge(node1, node2):
                return 0
            
            strength = 0
            strength += self.jaccard_coefficient(G, node1, node2)
            strength += self.adamic_adar_index(G, node1, node2)
            strength += self.resource_allocation_index(G, node1, node2)
            
            return strength / 3  # Normalize by the number of measures used
        except Exception as e:
            self.error_handler.handle_error(e, f"Error calculating edge strength between {node1} and {node2}")
            return 0

    def jaccard_coefficient(self, G, node1, node2):
        neighbors1 = set(G.neighbors(node1))
        neighbors2 = set(G.neighbors(node2))
        return len(neighbors1.intersection(neighbors2)) / len(neighbors1.union(neighbors2))

    def adamic_adar_index(self, G, node1, node2):
        return sum(1 / nx.log(G.degree(w)) for w in nx.common_neighbors(G, node1, node2))

    def resource_allocation_index(self, G, node1, node2):
        return sum(1 / G.degree(w) for w in nx.common_neighbors(G, node1, node2))

    def calculate_node_centrality(self, node):
        try:
            G = self.graph.to_networkx()
            centrality = nx.degree_centrality(G)[node]
            betweenness = nx.betweenness_centrality(G)[node]
            closeness = nx.closeness_centrality(G)[node]
            
            return (centrality + betweenness + closeness) / 3  # Normalize by the number of measures used
        except Exception as e:
            self.error_handler.handle_error(e, f"Error calculating node centrality for {node}")
            return 0

    def calculate_community_strength(self, community):
        try:
            G = self.graph.to_networkx()
            subgraph = G.subgraph(community)
            
            internal_edges = subgraph.number_of_edges()
            external_edges = sum(G.degree(n) for n in community) - 2 * internal_edges
            
            return internal_edges / (internal_edges + external_edges) if (internal_edges + external_edges) > 0 else 0
        except Exception as e:
            self.error_handler.handle_error(e, "Error calculating community strength")
            return 0