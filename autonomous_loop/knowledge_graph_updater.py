from .entity_extractor import EntityExtractor
from .relationship_extractor import RelationshipExtractor

class KnowledgeGraphUpdater:
    def __init__(self, knowledge_graph, logger, error_handler):
        self.knowledge_graph = knowledge_graph
        self.logger = logger
        self.error_handler = error_handler
        self.entity_extractor = EntityExtractor()
        self.relationship_extractor = RelationshipExtractor()

    async def update(self, scenario, action, outcome):
        try:
            entities = self.entity_extractor.extract(scenario, action, outcome)
            relationships = self.relationship_extractor.extract(scenario, action, outcome)

            self.logger.debug(f"Extracted entities: {entities}")
            self.logger.debug(f"Extracted relationships: {relationships}")

            for entity in entities:
                try:
                    self.logger.debug(f"Adding entity: {entity['name']} with properties: {entity['properties']}")
                    self._add_entity_safely(entity['name'], entity['properties'])
                except Exception as e:
                    self.logger.warning(f"Failed to add entity {entity['name']}: {str(e)}")
                    self.error_handler.handle_error(e, f"Failed to add entity {entity['name']}")

            for rel in relationships:
                try:
                    self.logger.debug(f"Adding relationship: {rel['type']} from {rel['start']} to {rel['end']} with properties: {rel['properties']}")
                    self._add_relationship_safely(rel['start'], rel['end'], rel['type'], rel['properties'])
                except Exception as e:
                    self.logger.warning(f"Failed to add relationship {rel['type']} from {rel['start']} to {rel['end']}: {str(e)}")
                    self.error_handler.handle_error(e, f"Failed to add relationship {rel['type']} from {rel['start']} to {rel['end']}")

            self.logger.info("Knowledge graph updated successfully")
        except Exception as e:
            self.error_handler.handle_error(e, "Error updating knowledge graph")

    def _add_entity_safely(self, name, properties):
        sanitized_properties = {k: v for k, v in properties.items() if isinstance(v, (str, int, float, bool))}
        self.knowledge_graph.add_entity(name, sanitized_properties)

    def _add_relationship_safely(self, start, end, rel_type, properties):
        sanitized_properties = {k: v for k, v in properties.items() if isinstance(v, (str, int, float, bool))}
        self.knowledge_graph.add_relationship(start, end, rel_type, sanitized_properties)