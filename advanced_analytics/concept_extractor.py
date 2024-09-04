import spacy
from collections import Counter
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class ConceptExtractor:
    def __init__(self):
        self.logger = Logger("ConceptExtractor")
        self.error_handler = ErrorHandler()
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except Exception as e:
            self.error_handler.handle_error(e, "Error loading spaCy model")
            self.nlp = None

    def extract_concepts(self, text):
        if not self.nlp:
            self.logger.error("spaCy model not loaded. Cannot extract concepts.")
            return []

        try:
            doc = self.nlp(text)
            concepts = []
            for chunk in doc.noun_chunks:
                if chunk.root.pos_ in ['NOUN', 'PROPN']:
                    concepts.append(chunk.text)
            return concepts
        except Exception as e:
            self.error_handler.handle_error(e, "Error extracting concepts")
            return []

    def get_top_concepts(self, text, top_n=10):
        concepts = self.extract_concepts(text)
        concept_counts = Counter(concepts)
        return concept_counts.most_common(top_n)

    def extract_named_entities(self, text):
        if not self.nlp:
            self.logger.error("spaCy model not loaded. Cannot extract named entities.")
            return []

        try:
            doc = self.nlp(text)
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            return entities
        except Exception as e:
            self.error_handler.handle_error(e, "Error extracting named entities")
            return []

    def extract_key_phrases(self, text, min_length=2, max_length=4):
        concepts = self.extract_concepts(text)
        key_phrases = [concept for concept in concepts if min_length <= len(concept.split()) <= max_length]
        return list(set(key_phrases))  # Remove duplicates