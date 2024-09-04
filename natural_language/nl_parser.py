import spacy
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class NLParser:
    def __init__(self):
        self.logger = Logger("NLParser")
        self.error_handler = ErrorHandler()
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except Exception as e:
            self.error_handler.handle_error(e, "Error loading spaCy model")
            self.nlp = None

    def parse(self, text):
        if not self.nlp:
            self.logger.error("spaCy model not loaded. Cannot parse text.")
            return None

        try:
            doc = self.nlp(text)
            return {
                'tokens': [token.text for token in doc],
                'entities': [(ent.text, ent.label_) for ent in doc.ents],
                'noun_chunks': [chunk.text for chunk in doc.noun_chunks],
                'dependencies': [(token.text, token.dep_, token.head.text) for token in doc]
            }
        except Exception as e:
            self.error_handler.handle_error(e, "Error parsing text")
            return None

    def extract_keywords(self, text):
        if not self.nlp:
            self.logger.error("spaCy model not loaded. Cannot extract keywords.")
            return None

        try:
            doc = self.nlp(text)
            return [token.text for token in doc if not token.is_stop and token.is_alpha]
        except Exception as e:
            self.error_handler.handle_error(e, "Error extracting keywords")
            return None

    def analyze_sentiment(self, text):
        if not self.nlp:
            self.logger.error("spaCy model not loaded. Cannot analyze sentiment.")
            return None

        try:
            doc = self.nlp(text)
            return sum([token.sentiment for token in doc]) / len(doc)
        except Exception as e:
            self.error_handler.handle_error(e, "Error analyzing sentiment")
            return None