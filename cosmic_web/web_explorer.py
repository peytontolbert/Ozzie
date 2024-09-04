class WebExplorer:
    def __init__(self, web_structure):
        self.web_structure = web_structure

    def explore_neighborhood(self, concept_id, depth=1):
        query = (
            f"MATCH (n)-[r*1..{depth}]-(m) "
            f"WHERE id(n) = $concept_id "
            f"RETURN n, r, m"
        )
        return self.web_structure.graph_structure.execute_query(query, {"concept_id": concept_id})

    def find_shortest_path(self, start_concept_id, end_concept_id):
        query = (
            "MATCH p=shortestPath((start)-[*]-(end)) "
            "WHERE id(start) = $start_id AND id(end) = $end_id "
            "RETURN p"
        )
        return self.web_structure.graph_structure.execute_query(query, {"start_id": start_concept_id, "end_id": end_concept_id})

    def get_most_connected_concepts(self, limit=10):
        query = (
            "MATCH (n)-[r]-() "
            "WITH n, count(r) as connections "
            "ORDER BY connections DESC "
            "LIMIT $limit "
            "RETURN n, connections"
        )
        return self.web_structure.graph_structure.execute_query(query, {"limit": limit})