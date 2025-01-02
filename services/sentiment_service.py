import pickle
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from utils.preprocess import preprocess_comment, get_sentiment_label

class SentimentService:
    def __init__(self):
        with open("models/model.pkl", "rb") as f:
            self.model = pickle.load(f)
        with open("models/vectorizer.pkl", "rb") as f:
            self.vectorizer = pickle.load(f)
        self.stopwords_english = set(stopwords.words("english"))
        self.stemmer = PorterStemmer()

    def preprocess_comment(self, comment):
        return preprocess_comment(comment, self.stopwords_english, self.stemmer)

    def get_sentiment(self, processed_comment):
        features = self.vectorizer.transform([processed_comment])
        prediction = self.model.predict(features)[0]
        return get_sentiment_label(prediction)

    def analyze_sentiments(self, comments):
        sentiments = {"positive": 0, "neutral": 0, "negative": 0}
        for comment in comments:
            processed_comment = self.preprocess_comment(comment)
            sentiment = self.get_sentiment(processed_comment)
            sentiments[sentiment] += 1

        total = sum(sentiments.values())
        if total == 0:
            return {"message": "No comments to analyze."}

        sentiment_percentages = {
            k: round(v / total * 100, 2) for k, v in sentiments.items()
        }
        return {"total_comments": total, "sentiments": sentiment_percentages}

