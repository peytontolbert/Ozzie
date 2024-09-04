class Edge:
    def __init__(self, start_node, end_node, relationship_type, properties=None):
        self.start_node = start_node
        self.end_node = end_node
        self.relationship_type = relationship_type
        self.properties = properties or {}

    def update_property(self, key, value):
        self.properties[key] = value

    def remove_property(self, key):
        if key in self.properties:
            del self.properties[key]

    def __str__(self):
        return f"Edge({self.start_node.id} -[{self.relationship_type}]-> {self.end_node.id})"