import requests
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class ExternalAPIIntegrator:
    def __init__(self):
        self.logger = Logger("ExternalAPIIntegrator")
        self.error_handler = ErrorHandler()

    def make_api_request(self, url, method='GET', params=None, headers=None, data=None):
        try:
            response = requests.request(method, url, params=params, headers=headers, data=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.error_handler.handle_error(e, f"API request failed: {url}")
            return None

    def integrate_data(self, api_data, knowledge_graph):
        # This method would be customized based on the specific API and data structure
        try:
            for item in api_data:
                # Example: Create a node for each item
                node_id = knowledge_graph.create_node(item['type'], item['properties'])
                self.logger.info(f"Created node: {node_id}")
                
                # Example: Create relationships based on item data
                for relation in item.get('relations', []):
                    target_id = knowledge_graph.create_node(relation['target_type'], relation['target_properties'])
                    knowledge_graph.create_relationship(node_id, target_id, relation['type'])
                    self.logger.info(f"Created relationship: {node_id} -> {target_id}")
            
            return True
        except Exception as e:
            self.error_handler.handle_error(e, "Error integrating API data into knowledge graph")
            return False