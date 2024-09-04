import networkx as nx
from datetime import datetime
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class KnowledgeEvolutionTracker:
    def __init__(self, graph_structure):
        self.graph = graph_structure
        self.logger = Logger("KnowledgeEvolutionTracker")
        self.error_handler = ErrorHandler()

    def track_node_changes(self, node_id, start_date, end_date):
        try:
            G = self.graph.to_networkx()
            node_history = G.nodes[node_id].get('history', [])
            relevant_history = [
                event for event in node_history 
                if start_date <= datetime.fromisoformat(event['timestamp']) <= end_date
            ]
            return relevant_history
        except Exception as e:
            self.error_handler.handle_error(e, f"Error tracking changes for node {node_id}")
            return []

    def track_relationship_changes(self, start_date, end_date):
        try:
            G = self.graph.to_networkx()
            relationship_changes = []
            for edge in G.edges():
                edge_data = G.get_edge_data(*edge)
                edge_history = edge_data.get('history', [])
                relevant_history = [
                    event for event in edge_history 
                    if start_date <= datetime.fromisoformat(event['timestamp']) <= end_date
                ]
                if relevant_history:
                    relationship_changes.append({
                        'source': edge[0],
                        'target': edge[1],
                        'changes': relevant_history
                    })
            return relationship_changes
        except Exception as e:
            self.error_handler.handle_error(e, "Error tracking relationship changes")
            return []

    def calculate_growth_rate(self, start_date, end_date):
        try:
            G_start = self.graph.get_snapshot(start_date)
            G_end = self.graph.get_snapshot(end_date)
            
            node_growth = (G_end.number_of_nodes() - G_start.number_of_nodes()) / G_start.number_of_nodes()
            edge_growth = (G_end.number_of_edges() - G_start.number_of_edges()) / G_start.number_of_edges()
            
            return {
                'node_growth_rate': node_growth,
                'edge_growth_rate': edge_growth
            }
        except Exception as e:
            self.error_handler.handle_error(e, "Error calculating growth rate")
            return None

    def identify_key_events(self, start_date, end_date, threshold=0.1):
        try:
            G = self.graph.to_networkx()
            key_events = []
            for node in G.nodes():
                node_history = G.nodes[node].get('history', [])
                relevant_history = [
                    event for event in node_history 
                    if start_date <= datetime.fromisoformat(event['timestamp']) <= end_date
                ]
                for event in relevant_history:
                    if event.get('importance', 0) > threshold:
                        key_events.append({
                            'node': node,
                            'event': event
                        })
            return sorted(key_events, key=lambda x: x['event']['importance'], reverse=True)
        except Exception as e:
            self.error_handler.handle_error(e, "Error identifying key events")
            return []