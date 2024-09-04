import spacy
from sklearn.metrics.pairwise import cosine_similarity
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class SemanticSimilarityCalculator:
    def __init__(self):
        self.logger = Logger("SemanticSimilarityCalculator")
        self.error_handler = ErrorHandler()
        try:
            self.nlp = spacy.load("en_core_web_lg")  # Use the large model for better word vectors
        except Exception as e:
            self.error_handler.handle_error(e, "Error loading spaCy model")
            self.nlp = None

    def calculate_similarity(self, text1, text2):
        if not self.nlp:
            self.logger.error("spaCy model not loaded. Cannot calculate similarity.")
            return 0

        try:
            doc1 = self.nlp(text1)
            doc2 = self.nlp(text2)
            return doc1.similarity(doc2)
        except Exception as e:
            self.error_handler.handle_error(e, "Error calculating similarity")
            return 0

    def calculate_word_similarity(self, word1, word2):
        if not self.nlp:
            self.logger.error("spaCy model not loaded. Cannot calculate word similarity.")
            return 0

        try:
            token1 = self.nlp(word1)[0]
            token2 = self.nlp(word2)[0]
            return token1.similarity(token2)
        except Exception as e:
            self.error_handler.handle_error(e, "Error calculating word similarity")
            return 0

    def find_most_similar(self, target_word, word_list):
        if not self.nlp:
            self.logger.error("spaCy model not loaded. Cannot find most similar word.")
            return None

        try:
            target_vector = self.nlp(target_word)[0].vector
            word_vectors = [self.nlp(word)[0].vector for word in word_list]
            similarities = cosine_similarity([target_vector], word_vectors)[0]
            most_similar_index = similarities.argmax()
            return word_list[most_similar_index], similarities[most_similar_index]
        except Exception as e:
            self.error_handler.handle_error(e, "Error finding most similar word")
            return None