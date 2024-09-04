from cosmic_web.node_connector import NodeConnector

class KnowledgeLinker:
    def __init__(self, web_structure):
        self.web_structure = web_structure
        self.node_connector = NodeConnector(web_structure)

    def link_similar_concepts(self, similarity_threshold=0.8):
        concepts = self.web_structure.graph_structure.get_all_nodes("Concept")
        for i, concept1 in enumerate(concepts):
            for concept2 in concepts[i+1:]:
                similarity = self.calculate_similarity(concept1, concept2)
                if similarity >= similarity_threshold:
                    self.node_connector.connect_nodes(concept1['id'], concept2['id'], "SIMILAR_TO", similarity)

    def link_by_co_occurrence(self, context_window=5):
        # This is a simplified version. In a real-world scenario, you'd analyze a large corpus of text.
        concepts = self.web_structure.graph_structure.get_all_nodes("Concept")
        concept_names = [c['name'] for c in concepts]
        for i, concept in enumerate(concept_names):
            start = max(0, i - context_window)
            end = min(len(concept_names), i + context_window + 1)
            context = concept_names[start:i] + concept_names[i+1:end]
            for co_concept in context:
                if concept != co_concept:
                    source_id = next(c['id'] for c in concepts if c['name'] == concept)
                    target_id = next(c['id'] for c in concepts if c['name'] == co_concept)
                    self.node_connector.connect_nodes(source_id, target_id, "CO_OCCURS_WITH")

    def calculate_similarity(self, concept1, concept2):
        # This is a placeholder. In a real-world scenario, you'd use more sophisticated similarity measures.
        return len(set(concept1['properties'].keys()) & set(concept2['properties'].keys())) / \
               len(set(concept1['properties'].keys()) | set(concept2['properties'].keys()))