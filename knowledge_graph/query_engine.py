class QueryEngine:
    def __init__(self, graph_structure):
        self.graph_structure = graph_structure

    def execute_query(self, query, parameters=None):
        with self.graph_structure.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

    def get_node_by_id(self, node_id):
        query = (
            "MATCH (n) "
            "WHERE id(n) = $node_id "
            "RETURN n"
        )
        result = self.execute_query(query, {"node_id": node_id})
        return result[0]['n'] if result else None

    def get_nodes_by_label(self, label):
        query = (
            f"MATCH (n:{label}) "
            "RETURN n"
        )
        return self.execute_query(query)

    def get_relationships(self, start_node_id, end_node_id=None, relationship_type=None):
        query = (
            "MATCH (a)-[r]->(b) "
            "WHERE id(a) = $start_id "
        )
        if end_node_id:
            query += "AND id(b) = $end_id "
        if relationship_type:
            query += f"AND type(r) = '{relationship_type}' "
        query += "RETURN r"
        
        parameters = {"start_id": start_node_id}
        if end_node_id:
            parameters["end_id"] = end_node_id
        
        return self.execute_query(query, parameters)