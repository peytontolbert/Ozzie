from gensim import corpora
from gensim.models import LdaModel
from gensim.parsing.preprocessing import STOPWORDS
from nltk.tokenize import word_tokenize
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class TopicModeler:
    def __init__(self):
        self.logger = Logger("TopicModeler")
        self.error_handler = ErrorHandler()
        self.dictionary = None
        self.lda_model = None

    def preprocess_text(self, text):
        try:
            tokens = word_tokenize(text.lower())
            return [token for token in tokens if token not in STOPWORDS and token.isalpha()]
        except Exception as e:
            self.error_handler.handle_error(e, "Error preprocessing text")
            return []

    def train_model(self, documents, num_topics=5, passes=15):
        try:
            preprocessed_docs = [self.preprocess_text(doc) for doc in documents]
            self.dictionary = corpora.Dictionary(preprocessed_docs)
            corpus = [self.dictionary.doc2bow(doc) for doc in preprocessed_docs]
            self.lda_model = LdaModel(corpus=corpus, id2word=self.dictionary, num_topics=num_topics, passes=passes)
            self.logger.info("LDA model trained successfully")
        except Exception as e:
            self.error_handler.handle_error(e, "Error training LDA model")

    def get_topics(self, num_words=10):
        if not self.lda_model:
            self.logger.error("LDA model not trained. Cannot get topics.")
            return []

        try:
            return self.lda_model.print_topics(num_words=num_words)
        except Exception as e:
            self.error_handler.handle_error(e, "Error getting topics")
            return []

    def infer_topics(self, text):
        if not self.lda_model or not self.dictionary:
            self.logger.error("LDA model or dictionary not initialized. Cannot infer topics.")
            return []

        try:
            bow = self.dictionary.doc2bow(self.preprocess_text(text))
            return self.lda_model[bow]
        except Exception as e:
            self.error_handler.handle_error(e, "Error inferring topics")
            return []