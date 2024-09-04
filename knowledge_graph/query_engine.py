from neo4j import GraphDatabase
from utils.logger import Logger
from utils.error_handler import ErrorHandler
import json

class QueryEngine:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.logger = Logger("QueryEngine")
        self.error_handler = ErrorHandler()

    def close(self):
        self.driver.close()

    def execute_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

    async def find_related_concepts(self, entities):
        query = """
        MATCH (e:Entity)-[:RELATED_TO]-(c:Concept)
        WHERE e.name IN $entities
        RETURN DISTINCT c.name AS concept
        """
        try:
            result = self.execute_query(query, {"entities": entities})
            return [record["concept"] for record in result]
        except Exception as e:
            self.error_handler.handle_error(e, "Error finding related concepts")
            return []

    def _sanitize_properties(self, properties):
        sanitized = {}
        for key, value in properties.items():
            if isinstance(value, (str, int, float, bool)):
                sanitized[key] = value
            elif isinstance(value, (list, dict)):
                sanitized[key] = json.dumps(value)
            else:
                sanitized[key] = str(value)
        return sanitized

    def add_entity(self, name, properties=None):
        sanitized_properties = self._sanitize_properties(properties or {})
        query = """
        MERGE (e:Entity {name: $name})
        ON CREATE SET e += $properties
        ON MATCH SET e += $properties
        RETURN e
        """
        self.execute_query(query, {"name": name, "properties": sanitized_properties})

    def add_relationship(self, start, end, relationship_type, properties):
        sanitized_properties = self._sanitize_properties(properties)
        query = f"""
        MATCH (start:Entity {{name: $start}})
        MATCH (end:Entity {{name: $end}})
        MERGE (start)-[r:{relationship_type}]->(end)
        SET r += $properties
        RETURN r
        """
        self.execute_query(query, {"start": start, "end": end, "properties": sanitized_properties})

    def get_entity_relationships(self, entity_name):
        query = """
        MATCH (e:Entity {name: $name})-[r]-(related)
        RETURN type(r) AS relationship_type, related.name AS related_entity
        """
        return self.execute_query(query, {"name": entity_name})

    def get_entity_by_name(self, name):
        query = """
        MATCH (e:Entity {name: $name})
        RETURN e
        """
        result = self.execute_query(query, {"name": name})
        return result[0]['e'] if result else None

    def update_entity_property(self, name, property_name, property_value):
        sanitized_value = self._sanitize_properties({property_name: property_value})[property_name]
        query = """
        MATCH (e:Entity {name: $name})
        SET e[$property_name] = $property_value
        RETURN e
        """
        self.execute_query(query, {"name": name, "property_name": property_name, "property_value": sanitized_value})

    def delete_entity(self, name):
        query = """
        MATCH (e:Entity {name: $name})
        DETACH DELETE e
        """
        self.execute_query(query, {"name": name})

    def get_all_entities(self):
        query = """
        MATCH (e:Entity)
        RETURN e
        """
        return self.execute_query(query)

    def get_entities_by_property(self, property_name, property_value):
        query = """
        MATCH (e:Entity)
        WHERE e[$property_name] = $property_value
        RETURN e
        """
        return self.execute_query(query, {"property_name": property_name, "property_value": property_value})

    def add_concept(self, name, properties=None):
        sanitized_properties = self._sanitize_properties(properties or {})
        query = """
        MERGE (c:Concept {name: $name})
        SET c += $properties
        RETURN c
        """
        self.execute_query(query, {"name": name, "properties": sanitized_properties})

    def relate_entity_to_concept(self, entity_name, concept_name, relationship_type="RELATED_TO", properties=None):
        sanitized_properties = self._sanitize_properties(properties or {})
        query = f"""
        MATCH (e:Entity {{name: $entity_name}})
        MATCH (c:Concept {{name: $concept_name}})
        MERGE (e)-[r:{relationship_type}]->(c)
        SET r += $properties
        RETURN r
        """
        self.execute_query(query, {"entity_name": entity_name, "concept_name": concept_name, "properties": sanitized_properties})

    def get_related_concepts(self, entity_name):
        query = """
        MATCH (e:Entity {name: $name})-[r:RELATED_TO]->(c:Concept)
        RETURN c.name AS concept, type(r) AS relationship_type, r AS relationship_properties
        """
        return self.execute_query(query, {"name": entity_name})

    # Add more graph-specific query methods as needed