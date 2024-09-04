import networkx as nx
import matplotlib.pyplot as plt

class GraphVisualizer:
    def __init__(self, graph_structure):
        self.graph_structure = graph_structure

    def visualize(self, limit=100):
        G = nx.Graph()
        
        # Fetch nodes and edges from the graph structure
        query = (
            f"MATCH (n) "
            f"WITH n LIMIT {limit} "
            f"MATCH (n)-[r]-(m) "
            f"RETURN n, r, m"
        )
        result = self.graph_structure.execute_query(query)

        for record in result:
            source = record['n']
            target = record['m']
            G.add_node(source['id'], label=source['label'])
            G.add_node(target['id'], label=target['label'])
            G.add_edge(source['id'], target['id'], type=record['r'].type)

        # Draw the graph
        pos = nx.spring_layout(G)
        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', 
                node_size=500, font_size=8, font_weight='bold')
        
        # Add edge labels
        edge_labels = nx.get_edge_attributes(G, 'type')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.title("Knowledge Graph Visualization")
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    def save_visualization(self, filename, limit=100):
        self.visualize(limit)
        plt.savefig(filename)
        plt.close()