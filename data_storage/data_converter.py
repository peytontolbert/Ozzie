import json

class DataConverter:
    @staticmethod
    def json_to_graph(json_data):
        data = json.loads(json_data)
        nodes = []
        edges = []

        for item in data:
            nodes.append({
                "id": item["id"],
                "label": item.get("label", "Node"),
                "properties": item.get("properties", {})
            })
            for relation in item.get("relations", []):
                edges.append({
                    "source": item["id"],
                    "target": relation["target"],
                    "type": relation["type"],
                    "properties": relation.get("properties", {})
                })

        return {"nodes": nodes, "edges": edges}

    @staticmethod
    def graph_to_json(graph_data):
        data = []
        node_map = {node["id"]: node for node in graph_data["nodes"]}

        for node in graph_data["nodes"]:
            node_data = {
                "id": node["id"],
                "label": node["label"],
                "properties": node["properties"],
                "relations": []
            }
            for edge in graph_data["edges"]:
                if edge["source"] == node["id"]:
                    node_data["relations"].append({
                        "target": edge["target"],
                        "type": edge["type"],
                        "properties": edge["properties"]
                    })
            data.append(node_data)

        return json.dumps(data, indent=2)

    @staticmethod
    def dict_to_graph(dict_data):
        nodes = []
        edges = []

        def process_dict(d, parent_id=None):
            node_id = len(nodes)
            nodes.append({
                "id": node_id,
                "label": "Dict",
                "properties": {"keys": list(d.keys())}
            })
            if parent_id is not None:
                edges.append({
                    "source": parent_id,
                    "target": node_id,
                    "type": "CONTAINS"
                })
            for key, value in d.items():
                if isinstance(value, dict):
                    process_dict(value, node_id)
                elif isinstance(value, list):
                    process_list(value, node_id)
                else:
                    leaf_id = len(nodes)
                    nodes.append({
                        "id": leaf_id,
                        "label": "Leaf",
                        "properties": {"key": key, "value": value}
                    })
                    edges.append({
                        "source": node_id,
                        "target": leaf_id,
                        "type": "HAS_PROPERTY"
                    })

        def process_list(l, parent_id):
            list_id = len(nodes)
            nodes.append({
                "id": list_id,
                "label": "List",
                "properties": {"length": len(l)}
            })
            edges.append({
                "source": parent_id,
                "target": list_id,
                "type": "CONTAINS"
            })
            for item in l:
                if isinstance(item, dict):
                    process_dict(item, list_id)
                elif isinstance(item, list):
                    process_list(item, list_id)
                else:
                    item_id = len(nodes)
                    nodes.append({
                        "id": item_id,
                        "label": "ListItem",
                        "properties": {"value": item}
                    })
                    edges.append({
                        "source": list_id,
                        "target": item_id,
                        "type": "CONTAINS"
                    })

        process_dict(dict_data)
        return {"nodes": nodes, "edges": edges}