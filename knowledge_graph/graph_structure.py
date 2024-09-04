from neo4j import GraphDatabase

class GraphStructure:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_node(self, label, properties):
        with self.driver.session() as session:
            result = session.write_transaction(self._create_node, label, properties)
            return result

    def create_relationship(self, start_node_id, end_node_id, relationship_type, properties=None):
        with self.driver.session() as session:
            result = session.write_transaction(self._create_relationship, start_node_id, end_node_id, relationship_type, properties)
            return result

    @staticmethod
    def _create_node(tx, label, properties):
        query = (
            f"CREATE (n:{label} $properties) "
            "RETURN id(n) AS node_id"
        )
        result = tx.run(query, properties=properties)
        return result.single()["node_id"]

    @staticmethod
    def _create_relationship(tx, start_node_id, end_node_id, relationship_type, properties):
        query = (
            "MATCH (a), (b) "
            "WHERE id(a) = $start_id AND id(b) = $end_id "
            f"CREATE (a)-[r:{relationship_type} $properties]->(b) "
            "RETURN type(r) AS relationship_type"
        )
        result = tx.run(query, start_id=start_node_id, end_id=end_node_id, properties=properties or {})
        return result.single()["relationship_type"]