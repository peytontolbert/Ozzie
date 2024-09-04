class Node:
    def __init__(self, id, label, properties):
        self.id = id
        self.label = label
        self.properties = properties

    def update_property(self, key, value):
        self.properties[key] = value

    def remove_property(self, key):
        if key in self.properties:
            del self.properties[key]

    def __str__(self):
        return f"Node(id={self.id}, label={self.label}, properties={self.properties})"