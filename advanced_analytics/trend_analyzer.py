import numpy as np
from scipy import stats
from utils.logger import Logger
from utils.error_handler import ErrorHandler
from datetime import datetime
class TrendAnalyzer:
    def __init__(self, graph_structure):
        self.graph = graph_structure
        self.logger = Logger("TrendAnalyzer")
        self.error_handler = ErrorHandler()

    def analyze_property_trend(self, property_name, start_date, end_date):
        try:
            G = self.graph.to_networkx()
            property_values = []
            timestamps = []
            
            for node in G.nodes():
                node_history = G.nodes[node].get('history', [])
                relevant_history = [
                    event for event in node_history 
                    if start_date <= event['timestamp'] <= end_date and property_name in event
                ]
                for event in relevant_history:
                    property_values.append(event[property_name])
                    timestamps.append(event['timestamp'])
            
            if not property_values:
                return None
            
            slope, intercept, r_value, p_value, std_err = stats.linregress(
                [t.timestamp() for t in timestamps], property_values
            )
            
            return {
                'slope': slope,
                'intercept': intercept,
                'r_value': r_value,
                'p_value': p_value,
                'std_err': std_err
            }
        except Exception as e:
            self.error_handler.handle_error(e, f"Error analyzing trend for property {property_name}")
            return None

    def detect_emerging_concepts(self, threshold=0.1, time_window=30):
        try:
            G = self.graph.to_networkx()
            concept_counts = {}
            total_concepts = 0
            
            for node in G.nodes():
                creation_time = G.nodes[node].get('creation_time')
                if creation_time and (datetime.now() - creation_time).days <= time_window:
                    concept = G.nodes[node].get('concept')
                    if concept:
                        concept_counts[concept] = concept_counts.get(concept, 0) + 1
                        total_concepts += 1
            
            emerging_concepts = [
                concept for concept, count in concept_counts.items()
                if count / total_concepts > threshold
            ]
            
            return emerging_concepts
        except Exception as e:
            self.error_handler.handle_error(e, "Error detecting emerging concepts")
            return []

    def analyze_relationship_trends(self, start_date, end_date):
        try:
            G = self.graph.to_networkx()
            relationship_counts = {}
            
            for edge in G.edges():
                edge_data = G.get_edge_data(*edge)
                edge_history = edge_data.get('history', [])
                relevant_history = [
                    event for event in edge_history 
                    if start_date <= event['timestamp'] <= end_date
                ]
                for event in relevant_history:
                    rel_type = event.get('type')
                    if rel_type:
                        relationship_counts[rel_type] = relationship_counts.get(rel_type, 0) + 1
            
            total_relationships = sum(relationship_counts.values())
            relationship_trends = {
                rel_type: count / total_relationships
                for rel_type, count in relationship_counts.items()
            }
            
            return relationship_trends
        except Exception as e:
            self.error_handler.handle_error(e, "Error analyzing relationship trends")
            return {}