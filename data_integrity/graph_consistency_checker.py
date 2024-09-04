from neo4j import GraphDatabase
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class GraphConsistencyChecker:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.logger = Logger("GraphConsistencyChecker")
        self.error_handler = ErrorHandler()

    def check_orphan_nodes(self):
        with self.driver.session() as session:
            result = session.run("MATCH (n) WHERE NOT (n)--() RETURN count(n) as orphan_count")
            orphan_count = result.single()["orphan_count"]
            if orphan_count > 0:
                self.logger.warning(f"Found {orphan_count} orphan nodes in the graph")
            else:
                self.logger.info("No orphan nodes found in the graph")

    def check_relationship_consistency(self):
        with self.driver.session() as session:
            result = session.run("MATCH ()-[r]->() WITH type(r) as type, count(*) as count RETURN type, count")
            for record in result:
                self.logger.info(f"Relationship type '{record['type']}' has {record['count']} instances")

    def check_property_consistency(self, label, property_name):
        with self.driver.session() as session:
            result = session.run(f"MATCH (n:{label}) WHERE NOT EXISTS(n.{property_name}) RETURN count(n) as missing_count")
            missing_count = result.single()["missing_count"]
            if missing_count > 0:
                self.logger.warning(f"Found {missing_count} nodes with label '{label}' missing the '{property_name}' property")
            else:
                self.logger.info(f"All nodes with label '{label}' have the '{property_name}' property")

    def run_all_checks(self):
        self.logger.info("Starting graph consistency checks...")
        self.check_orphan_nodes()
        self.check_relationship_consistency()
        self.check_property_consistency("Concept", "name")  # Example check
        self.logger.info("Graph consistency checks completed.")

    def close(self):
        self.driver.close()