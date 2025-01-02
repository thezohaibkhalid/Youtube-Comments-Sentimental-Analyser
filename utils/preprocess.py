import logging
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

logger = logging.getLogger(__name__)

def remove_stopwords(text, stopwords):
    words = [word for word in text.split() if word not in stopwords]
    return " ".join(words)

def stem_words(text, stemmer):
    words = [stemmer.stem(word) for word in text.split()]
    return " ".join(words)

def preprocess_comment(comment, stopwords_english, stemmer, apply_stemming=False):
    comment = comment.lower()
    comment = comment.translate(str.maketrans("", "", string.punctuation))
    comment = remove_stopwords(comment, stopwords_english)
    if apply_stemming and stemmer:
        comment = stem_words(comment, stemmer)
    return comment

def preprocess_file_content(content, apply_stemming=False):
    if not isinstance(content, str):
        logger.error("TypeError: Content must be a string.")
        raise TypeError("Content must be a string.")
    
    if not content.strip():
        logger.error("ValueError: Content is empty.")
        raise ValueError("Content is empty.")
    
    stopwords_english = set(stopwords.words("english"))
    stemmer = PorterStemmer() if apply_stemming else None
    processed_content = preprocess_comment(content, stopwords_english, stemmer, apply_stemming)
    logger.debug(f"Processed Content: {processed_content[:100]}...")  # First 100 chars
    
    if not processed_content.strip():
        logger.error("ValueError: No valid content after preprocessing.")
        raise ValueError("No valid content after preprocessing.")
    
    return processed_content

#Example Usage
#logging.basicConfig(level=logging.DEBUG)
#content = "This is a sample comment with some punctuation! and stop words."
#processed_content = preprocess_file_content(content, apply_stemming=True)
#print(processed_content)

def get_sentiment_label(prediction):
    labels = {0: "negative", 1: "neutral", 2: "positive"}
    return labels.get(prediction, "unknown")

