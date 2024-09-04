from neo4j import GraphDatabase
from data_storage.data_store import DataStore

class Neo4jDatabase(DataStore):
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def save(self, key, value):
        with self.driver.session() as session:
            session.write_transaction(self._create_or_update_node, key, value)

    def load(self, key):
        with self.driver.session() as session:
            return session.read_transaction(self._get_node, key)

    def delete(self, key):
        with self.driver.session() as session:
            session.write_transaction(self._delete_node, key)

    def exists(self, key):
        with self.driver.session() as session:
            return session.read_transaction(self._node_exists, key)

    @staticmethod
    def _create_or_update_node(tx, key, value):
        query = (
            "MERGE (n:Data {key: $key}) "
            "SET n.value = $value "
            "RETURN n"
        )
        result = tx.run(query, key=key, value=value)
        return result.single()

    @staticmethod
    def _get_node(tx, key):
        query = "MATCH (n:Data {key: $key}) RETURN n.value"
        result = tx.run(query, key=key)
        record = result.single()
        return record["n.value"] if record else None

    @staticmethod
    def _delete_node(tx, key):
        query = "MATCH (n:Data {key: $key}) DELETE n"
        tx.run(query, key=key)

    @staticmethod
    def _node_exists(tx, key):
        query = "MATCH (n:Data {key: $key}) RETURN COUNT(n) > 0 AS exists"
        result = tx.run(query, key=key)
        return result.single()["exists"]

    def close(self):
        self.driver.close()