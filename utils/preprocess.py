# utils/preprocess.py

import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Ensure NLTK data is downloaded
nltk.download('stopwords', quiet=True)

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def preprocess_comment(comment, apply_stemming=False):
    """
    Preprocesses a single comment by removing punctuation,
    converting to lowercase, removing stopwords, and optionally stemming.

    Args:
        comment (str): The comment text to preprocess.
        apply_stemming (bool): Whether to apply stemming.

    Returns:
        str: The preprocessed comment.
    """
    # Convert to lowercase
    comment = comment.lower()
    
    # Remove punctuation
    translator = str.maketrans('', '', string.punctuation)
    comment = comment.translate(translator)
    
    # Remove stopwords
    tokens = comment.split()
    tokens = [word for word in tokens if word not in stop_words]
    
    # Apply stemming if required
    if apply_stemming:
        tokens = [stemmer.stem(word) for word in tokens]
    
    # Rejoin tokens
    processed_comment = ' '.join(tokens)
    
    return processed_comment

def preprocess_text(lines, apply_stemming=False):
    """
    Preprocesses a list of text lines by removing punctuation,
    converting to lowercase, removing stopwords, and optionally stemming.

    Args:
        lines (list of str): The lines of text to preprocess.
        apply_stemming (bool): Whether to apply stemming.

    Returns:
        list of str: The preprocessed text lines.
    """
    processed = []
    for line in lines:
        processed_line = preprocess_comment(line, apply_stemming)
        if processed_line:
            processed.append(processed_line)
    return processed

def get_sentiment_label(prediction):
    """
    Maps a numerical prediction to a sentiment label.

    Args:
        prediction (int): The numerical sentiment prediction.

    Returns:
        str: The corresponding sentiment label.
    """
    labels = {0: "negative", 1: "neutral", 2: "positive"}
    return labels.get(prediction, "unknown")
