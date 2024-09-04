from knowledge_graph.graph_structure import GraphStructure

class WebStructure:
    def __init__(self, graph_structure):
        self.graph_structure = graph_structure

    def add_concept(self, concept_name, properties=None):
        return self.graph_structure.create_node("Concept", {"name": concept_name, **(properties or {})})

    def add_relationship(self, source_concept_id, target_concept_id, relationship_type, properties=None):
        return self.graph_structure.create_relationship(source_concept_id, target_concept_id, relationship_type, properties)

    def get_concept(self, concept_id):
        return self.graph_structure.get_node_by_id(concept_id)

    def get_relationships(self, concept_id):
        return self.graph_structure.get_relationships(concept_id)

    def update_concept(self, concept_id, properties):
        return self.graph_structure.update_node(concept_id, properties)

    def delete_concept(self, concept_id):
        return self.graph_structure.delete_node(concept_id)

    def delete_relationship(self, relationship_id):
        return self.graph_structure.delete_relationship(relationship_id)