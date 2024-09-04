class InferenceEngine:
    def __init__(self, web_structure):
        self.web_structure = web_structure

    def infer_transitive_relationships(self, relationship_type):
        query = (
            f"MATCH (a)-[:{relationship_type}]->(b)-[:{relationship_type}]->(c) "
            f"WHERE NOT (a)-[:{relationship_type}]->(c) "
            f"CREATE (a)-[r:{relationship_type}]->(c) "
            f"RETURN count(r) as new_relationships"
        )
        result = self.web_structure.graph_structure.execute_query(query)
        return result[0]['new_relationships']

    def infer_symmetric_relationships(self, relationship_type):
        query = (
            f"MATCH (a)-[r:{relationship_type}]->(b) "
            f"WHERE NOT (b)-[:{relationship_type}]->(a) "
            f"CREATE (b)-[r2:{relationship_type}]->(a) "
            f"RETURN count(r2) as new_relationships"
        )
        result = self.web_structure.graph_structure.execute_query(query)
        return result[0]['new_relationships']

    def infer_hierarchical_relationships(self):
        query = (
            "MATCH (a)-[:IS_A]->(b)-[:IS_A]->(c) "
            "WHERE NOT (a)-[:IS_A]->(c) "
            "CREATE (a)-[r:IS_A]->(c) "
            "RETURN count(r) as new_relationships"
        )
        result = self.web_structure.graph_structure.execute_query(query)
        return result[0]['new_relationships']

    def apply_rule_based_inference(self, rules):
        inferred_relationships = 0
        for rule in rules:
            query = (
                f"MATCH {rule['pattern']} "
                f"WHERE NOT {rule['condition']} "
                f"CREATE {rule['creation']} "
                f"RETURN count(*) as new_relationships"
            )
            result = self.web_structure.graph_structure.execute_query(query)
            inferred_relationships += result[0]['new_relationships']
        return inferred_relationships