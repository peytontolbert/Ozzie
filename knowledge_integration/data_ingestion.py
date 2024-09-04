import json
from cosmic_web.web_structure import WebStructure

class DataIngestion:
    def __init__(self, web_structure):
        self.web_structure = web_structure

    def ingest_json(self, json_data):
        data = json.loads(json_data)
        for item in data:
            concept_id = self.web_structure.add_concept(item['name'], item.get('properties'))
            for relation in item.get('relations', []):
                target_id = self.web_structure.add_concept(relation['target'])
                self.web_structure.add_relationship(concept_id, target_id, relation['type'])

    def ingest_text(self, text, nlp_processor):
        # This is a simplified version. In a real-world scenario, you'd use more advanced NLP techniques.
        entities = nlp_processor.extract_entities(text)
        relationships = nlp_processor.extract_relationships(text)

        entity_ids = {}
        for entity in entities:
            entity_ids[entity] = self.web_structure.add_concept(entity)

        for rel in relationships:
            if rel['source'] in entity_ids and rel['target'] in entity_ids:
                self.web_structure.add_relationship(entity_ids[rel['source']], entity_ids[rel['target']], rel['type'])

    def ingest_structured_data(self, data, schema):
        for item in data:
            concept_id = self.web_structure.add_concept(item[schema['name_field']], item)
            for relation_field in schema.get('relation_fields', []):
                if relation_field in item:
                    target_id = self.web_structure.add_concept(item[relation_field])
                    self.web_structure.add_relationship(concept_id, target_id, relation_field)