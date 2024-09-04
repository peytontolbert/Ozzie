from utils.logger import Logger
from utils.error_handler import ErrorHandler

class OntologyMapper:
    def __init__(self):
        self.logger = Logger("OntologyMapper")
        self.error_handler = ErrorHandler()
        self.ontology = {}  # This would be loaded from a file or database in a real implementation

    def load_ontology(self, ontology_file):
        try:
            # In a real implementation, this would parse an OWL or RDF file
            # For this example, we'll use a simple dictionary
            self.ontology = {
                "Person": {"properties": ["name", "age"], "relationships": ["knows", "worksFor"]},
                "Organization": {"properties": ["name", "location"], "relationships": ["employs"]},
                "Project": {"properties": ["name", "startDate"], "relationships": ["involves"]}
            }
            self.logger.info("Ontology loaded successfully")
        except Exception as e:
            self.error_handler.handle_error(e, f"Error loading ontology from {ontology_file}")

    def map_concept(self, concept_name):
        try:
            for ontology_concept, details in self.ontology.items():
                if concept_name.lower() == ontology_concept.lower():
                    return ontology_concept
            return None
        except Exception as e:
            self.error_handler.handle_error(e, f"Error mapping concept: {concept_name}")
            return None

    def get_concept_properties(self, concept_name):
        mapped_concept = self.map_concept(concept_name)
        if mapped_concept:
            return self.ontology[mapped_concept].get("properties", [])
        return []

    def get_concept_relationships(self, concept_name):
        mapped_concept = self.map_concept(concept_name)
        if mapped_concept:
            return self.ontology[mapped_concept].get("relationships", [])
        return []

    def apply_ontology_to_knowledge_graph(self, knowledge_graph):
        try:
            for node in knowledge_graph.get_all_nodes():
                mapped_concept = self.map_concept(node.label)
                if mapped_concept:
                    # Update node label to match ontology
                    node.label = mapped_concept
                    
                    # Add missing properties
                    for prop in self.get_concept_properties(mapped_concept):
                        if prop not in node.properties:
                            node.properties[prop] = None
                    
                    # Remove properties not in ontology
                    node.properties = {k: v for k, v in node.properties.items() if k in self.get_concept_properties(mapped_concept)}
                    
                    knowledge_graph.update_node(node)
            
            self.logger.info("Ontology applied to knowledge graph successfully")
            return True
        except Exception as e:
            self.error_handler.handle_error(e, "Error applying ontology to knowledge graph")
            return False