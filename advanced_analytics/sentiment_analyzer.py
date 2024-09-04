from textblob import TextBlob
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class SentimentAnalyzer:
    def __init__(self):
        self.logger = Logger("SentimentAnalyzer")
        self.error_handler = ErrorHandler()

    def analyze_sentiment(self, text):
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            if polarity > 0:
                sentiment = "Positive"
            elif polarity < 0:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"
            
            return {
                "sentiment": sentiment,
                "polarity": polarity,
                "subjectivity": subjectivity
            }
        except Exception as e:
            self.error_handler.handle_error(e, "Error analyzing sentiment")
            return None

    def analyze_sentence_sentiments(self, text):
        try:
            blob = TextBlob(text)
            sentence_sentiments = []
            for sentence in blob.sentences:
                sentiment = "Positive" if sentence.sentiment.polarity > 0 else "Negative" if sentence.sentiment.polarity < 0 else "Neutral"
                sentence_sentiments.append({
                    "sentence": str(sentence),
                    "sentiment": sentiment,
                    "polarity": sentence.sentiment.polarity,
                    "subjectivity": sentence.sentiment.subjectivity
                })
            return sentence_sentiments
        except Exception as e:
            self.error_handler.handle_error(e, "Error analyzing sentence sentiments")
            return []

    def get_overall_sentiment(self, text):
        analysis = self.analyze_sentiment(text)
        if analysis:
            return analysis["sentiment"]
        return None