from collections import Counter

class WebAnalyzer:
    def __init__(self, web_structure):
        self.web_structure = web_structure

    def analyze_concept_frequency(self):
        query = (
            "MATCH (n:Concept) "
            "RETURN n.name AS concept, count(*) AS frequency "
            "ORDER BY frequency DESC"
        )
        result = self.web_structure.graph_structure.execute_query(query)
        return {record['concept']: record['frequency'] for record in result}

    def analyze_relationship_types(self):
        query = (
            "MATCH ()-[r]->() "
            "RETURN type(r) AS relationship_type, count(*) AS frequency "
            "ORDER BY frequency DESC"
        )
        result = self.web_structure.graph_structure.execute_query(query)
        return {record['relationship_type']: record['frequency'] for record in result}

    def identify_central_concepts(self, limit=10):
        query = (
            "MATCH (n:Concept) "
            "WITH n, size((n)--()) AS degree "
            "ORDER BY degree DESC "
            "LIMIT $limit "
            "RETURN n.name AS concept, degree"
        )
        return self.web_structure.graph_structure.execute_query(query, {"limit": limit})

    def analyze_concept_clusters(self):
        # This is a simplified clustering method. For more advanced clustering,
        # you might want to use a graph clustering algorithm like Louvain or Label Propagation.
        query = (
            "MATCH (n:Concept)-[:RELATED_TO]-(m:Concept) "
            "WITH n, collect(m) AS related_concepts "
            "RETURN n.name AS concept, [c IN related_concepts | c.name] AS cluster"
        )
        result = self.web_structure.graph_structure.execute_query(query)
        clusters = {}
        for record in result:
            concept = record['concept']
            cluster = record['cluster']
            for c in cluster:
                if c not in clusters:
                    clusters[c] = set()
                clusters[c].add(concept)
                clusters[c].update(cluster)
        return clusters