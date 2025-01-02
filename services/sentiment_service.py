# services/sentiment_service.py

import pickle
from utils.preprocess import get_sentiment_label, preprocess_comment  # Import preprocess_comment
import logging

# Define the logger for this module
logger = logging.getLogger(__name__)

class SentimentService:
    def __init__(self):
        # Load the trained model and vectorizer
        try:
            with open("models/model.pkl", "rb") as f:
                self.model = pickle.load(f)
            with open("models/vectorizer.pkl", "rb") as f:
                self.vectorizer = pickle.load(f)
            logger.info("Model and vectorizer loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading model or vectorizer: {e}")
            raise e  # Re-raise exception after logging

    def preprocess_comment(self, comment):
        """
        Preprocesses a single comment.

        Args:
            comment (str): The comment text to preprocess.

        Returns:
            str: The preprocessed comment.
        """
        return preprocess_comment(comment, apply_stemming=False)  # Disabled stemming

    def get_sentiment(self, processed_comment):
        """
        Predicts the sentiment of a preprocessed comment.

        Args:
            processed_comment (str): The preprocessed comment text.

        Returns:
            str: The sentiment label ("positive", "neutral", "negative").
        """
        features = self.vectorizer.transform([processed_comment])
        prediction = self.model.predict(features)[0]
        sentiment = get_sentiment_label(prediction)
        logger.debug(f"Processed Comment: {processed_comment}")
        logger.debug(f"Predicted Sentiment: {sentiment}")
        return sentiment

    def analyze_sentiments(self, comments):
        """
        Analyzes the sentiments of a list of comments.

        Args:
            comments (list of str): The list of comment texts.

        Returns:
            dict: A dictionary containing total comments and sentiment percentages.
        """
        sentiments = {"positive": 0, "neutral": 0, "negative": 0}
        unknown_count = 0
        for comment in comments:
            sentiment = self.get_sentiment(comment)
            if sentiment in sentiments:
                sentiments[sentiment] += 1
            else:
                unknown_count += 1
                logger.warning(f"Unknown sentiment label: {sentiment}")

        total = sum(sentiments.values())
        logger.debug(f"Total sentiments counted: {total}")
        if unknown_count > 0:
            logger.warning(f"Number of unknown sentiments: {unknown_count}")
        
        if total == 0:
            logger.error("No valid sentiments were detected.")
            return {"message": "No comments to analyze."}

        sentiment_percentages = {
            k: round(v / total * 100, 2) for k, v in sentiments.items()
        }
        if unknown_count > 0:
            sentiment_percentages["unknown"] = round(unknown_count / (total + unknown_count) * 100, 2)
        logger.info(f"Sentiment analysis completed: {sentiment_percentages}")
        return {"total_comments": total, "sentiments": sentiment_percentages}
