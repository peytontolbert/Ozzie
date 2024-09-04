import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class SemanticDistanceCalculator:
    def __init__(self, graph_structure):
        self.graph = graph_structure
        self.logger = Logger("SemanticDistanceCalculator")
        self.error_handler = ErrorHandler()
        self.vectorizer = TfidfVectorizer()

    def calculate_semantic_distance(self, node1, node2):
        try:
            content1 = self.get_node_content(node1)
            content2 = self.get_node_content(node2)
            
            if not content1 or not content2:
                return 1.0  # Maximum distance if content is missing
            
            vectors = self.vectorizer.fit_transform([content1, content2])
            similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
            
            return 1.0 - similarity  # Convert similarity to distance
        except Exception as e:
            self.error_handler.handle_error(e, f"Error calculating semantic distance between {node1} and {node2}")
            return 1.0

    def get_node_content(self, node):
        # This method should be implemented to extract textual content from a node
        # For now, we'll use a placeholder implementation
        return self.graph.get_node_attribute(node, 'content', '')

    def calculate_semantic_distances_matrix(self, nodes):
        try:
            contents = [self.get_node_content(node) for node in nodes]
            vectors = self.vectorizer.fit_transform(contents)
            similarity_matrix = cosine_similarity(vectors)
            distance_matrix = 1.0 - similarity_matrix
            return distance_matrix
        except Exception as e:
            self.error_handler.handle_error(e, "Error calculating semantic distances matrix")
            return np.ones((len(nodes), len(nodes)))

    def find_semantically_similar_nodes(self, target_node, threshold=0.2):
        try:
            target_content = self.get_node_content(target_node)
            all_nodes = self.graph.get_all_nodes()
            all_contents = [self.get_node_content(node) for node in all_nodes]
            
            vectors = self.vectorizer.fit_transform([target_content] + all_contents)
            similarities = cosine_similarity(vectors[0], vectors[1:]).flatten()
            
            similar_nodes = [(node, 1.0 - sim) for node, sim in zip(all_nodes, similarities) if sim >= (1.0 - threshold)]
            return sorted(similar_nodes, key=lambda x: x[1])
        except Exception as e:
            self.error_handler.handle_error(e, f"Error finding semantically similar nodes to {target_node}")
            return []