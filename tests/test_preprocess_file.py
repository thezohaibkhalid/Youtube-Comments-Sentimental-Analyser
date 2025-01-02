# tests/test_preprocess_file.py

import unittest
from utils.preprocess import preprocess_comment, get_sentiment_label
from services.sentiment_service import SentimentService

class TestPreprocessFileContent(unittest.TestCase):
    def test_preprocess_comment(self):
        input_text = "I absolutely love this! It's fantastic and works great."
        expected_output = "absolutely love fantastic works great"
        self.assertEqual(preprocess_comment(input_text), expected_output)
    
    def test_preprocess_comment_with_stemming(self):
        #  stem_words is used within preprocess_comment
        input_text = "Running runs ran runner easily"
        expected_output = "run run ran runner easili"
        self.assertEqual(preprocess_comment(input_text), expected_output)
    
    def test_remove_stopwords(self):
        # Directly testing remove_stopwords if exposed, otherwise test via preprocess_comment
        input_text = "I am testing the stopwords removal functionality."
        expected_output = "testing stopwords removal functionality"
        self.assertEqual(preprocess_comment(input_text), expected_output)
    
    def test_stem_words(self):
        # Directly testing stem_words if exposed, otherwise test via preprocess_comment
        input_text = "Technology has transformed the way we live."
        expected_output = "technolog transform way live"
        self.assertEqual(preprocess_comment(input_text), expected_output)
    
    def test_get_sentiment_label(self):
        self.assertEqual(get_sentiment_label(0), "negative")
        self.assertEqual(get_sentiment_label(1), "neutral")
        self.assertEqual(get_sentiment_label(2), "positive")
        self.assertEqual(get_sentiment_label(3), "unknown")
        self.assertEqual(get_sentiment_label("positive"), "positive")
        self.assertEqual(get_sentiment_label("NEGATIVE"), "negative")
        self.assertEqual(get_sentiment_label("UnknownLabel"), "unknown")
    
    def test_sentiment_service(self):
        # This requires a mock model and vectorizer
        # For simplicity, we'll skip detailed mocking here
        service = SentimentService()
        comment = "I love this product!"
        sentiment = service.get_sentiment(comment)
        self.assertIn(sentiment, ["positive", "neutral", "negative", "unknown"])
    
    def test_analyze_sentiments(self):
        service = SentimentService()
        comments = [
            "I love this product!",
            "This is the worst experience ever.",
            "It's okay, not great but not bad."
        ]
        result = service.analyze_sentiments(comments)
        self.assertEqual(result["total_comments"], 3)
        self.assertIn("positive", result["sentiments"])
        self.assertIn("neutral", result["sentiments"])
        self.assertIn("negative", result["sentiments"])
        # Since we can't predict exact percentages, just check if they sum up correctly
        total_percentage = sum(result["sentiments"].values())
        self.assertAlmostEqual(total_percentage, 100.0, places=1)

if __name__ == '__main__':
    unittest.main()
