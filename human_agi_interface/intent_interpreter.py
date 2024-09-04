import spacy
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class IntentInterpreter:
    def __init__(self):
        self.logger = Logger("IntentInterpreter")
        self.error_handler = ErrorHandler()
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except Exception as e:
            self.error_handler.handle_error(e, "Error loading spaCy model")
            self.nlp = None

    def interpret_intent(self, user_input):
        if not self.nlp:
            self.logger.error("spaCy model not loaded. Cannot interpret intent.")
            return None

        try:
            doc = self.nlp(user_input)
            
            # Extract main verb and its object
            main_verb = None
            main_object = None
            for token in doc:
                if token.dep_ == "ROOT" and token.pos_ == "VERB":
                    main_verb = token.lemma_
                if token.dep_ in ["dobj", "pobj"] and not main_object:
                    main_object = token.text

            # Identify entities
            entities = [(ent.text, ent.label_) for ent in doc.ents]

            # Determine overall sentiment
            sentiment = doc.sentiment

            intent = {
                "action": main_verb,
                "object": main_object,
                "entities": entities,
                "sentiment": sentiment
            }

            self.logger.info(f"Interpreted intent: {intent}")
            return intent
        except Exception as e:
            self.error_handler.handle_error(e, "Error interpreting intent")
            return None

    def classify_intent(self, intent):
        try:
            if intent["action"] in ["search", "find", "look"]:
                return "QUERY"
            elif intent["action"] in ["create", "make", "generate"]:
                return "CREATE"
            elif intent["action"] in ["update", "modify", "change"]:
                return "UPDATE"
            elif intent["action"] in ["delete", "remove", "erase"]:
                return "DELETE"
            else:
                return "UNKNOWN"
        except Exception as e:
            self.error_handler.handle_error(e, "Error classifying intent")
            return "UNKNOWN"

    def extract_parameters(self, intent):
        try:
            parameters = {}
            for entity in intent["entities"]:
                if entity[1] in ["PERSON", "ORG", "GPE"]:
                    parameters["subject"] = entity[0]
                elif entity[1] in ["DATE", "TIME"]:
                    parameters["time"] = entity[0]
                elif entity[1] == "CARDINAL":
                    parameters["quantity"] = entity[0]
            return parameters
        except Exception as e:
            self.error_handler.handle_error(e, "Error extracting parameters")
            return {}