from cosmic_web.web_structure import WebStructure

class NodeConnector:
    def __init__(self, web_structure):
        self.web_structure = web_structure

    def connect_nodes(self, source_id, target_id, relationship_type, strength=1.0):
        properties = {"strength": strength}
        return self.web_structure.add_relationship(source_id, target_id, relationship_type, properties)

    def strengthen_connection(self, relationship_id, increment=0.1):
        relationship = self.web_structure.graph_structure.get_relationship_by_id(relationship_id)
        if relationship:
            current_strength = relationship.get("strength", 1.0)
            new_strength = min(current_strength + increment, 1.0)
            self.web_structure.graph_structure.update_relationship(relationship_id, {"strength": new_strength})
            return new_strength
        return None

    def weaken_connection(self, relationship_id, decrement=0.1):
        relationship = self.web_structure.graph_structure.get_relationship_by_id(relationship_id)
        if relationship:
            current_strength = relationship.get("strength", 1.0)
            new_strength = max(current_strength - decrement, 0.0)
            self.web_structure.graph_structure.update_relationship(relationship_id, {"strength": new_strength})
            return new_strength
        return None