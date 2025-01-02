# utils/preprocess.py

import string
import logging
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

# Initialize logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the desired logging level

# Create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create formatter and add to handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# Add handler to logger if it doesn't already have one
if not logger.handlers:
    logger.addHandler(ch)

# Ensure NLTK data is downloaded
try:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)  # For sentence tokenization if needed
    stop_words = set(stopwords.words('english'))
    logger.info("NLTK stopwords and punkt tokenizer downloaded successfully.")
except Exception as e:
    logger.error(f"Error downloading NLTK data: {e}")
    stop_words = set()

# Initialize the Porter Stemmer
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

    Raises:
        TypeError: If the comment is not a string.
    """
    if not isinstance(comment, str):
        logger.error("TypeError: Comment must be a string.")
        raise TypeError("Comment must be a string.")
    
    # Convert to lowercase
    comment = comment.lower()
    logger.debug(f"Lowercased Comment: {comment[:50]}...")  # Show first 50 chars for brevity
    
    # Remove punctuation
    translator = str.maketrans('', '', string.punctuation)
    comment = comment.translate(translator)
    logger.debug(f"Comment after Punctuation Removal: {comment[:50]}...")  # First 50 chars
    
    # Tokenization
    tokens = comment.split()
    logger.debug(f"Tokenized Comment: {tokens[:10]}...")  # Show first 10 tokens
    
    # Remove stopwords
    tokens = [word for word in tokens if word not in stop_words]
    logger.debug(f"Comment after Stopwords Removal: {tokens[:10]}...")  # First 10 tokens
    
    # Apply stemming if required
    if apply_stemming:
        tokens = [stemmer.stem(word) for word in tokens]
        logger.debug(f"Comment after Stemming: {tokens[:10]}...")  # First 10 tokens
    
    # Rejoin tokens
    processed_comment = ' '.join(tokens)
    logger.debug(f"Processed Comment: {processed_comment[:100]}...")  # First 100 chars
    
    return processed_comment

def preprocess_file_content(content, apply_stemming=False):
    """
    Preprocesses the entire file content by removing punctuation,
    converting to lowercase, removing stopwords, and optionally stemming.

    Args:
        content (str): The entire text content of the file to preprocess.
        apply_stemming (bool): Whether to apply stemming.

    Returns:
        str: The preprocessed text content.

    Raises:
        TypeError: If the content is not a string.
        ValueError: If the content is empty after preprocessing.
    """
    # Type Check
    if not isinstance(content, str):
        logger.error("TypeError: Content must be a string.")
        raise TypeError("Content must be a string.")
    
    # Empty Content Check
    if not content.strip():
        logger.error("ValueError: Content is empty.")
        raise ValueError("Content is empty.")
    
    # Lowercasing
    content = content.lower()
    logger.debug(f"Lowercased Content: {content[:100]}...")  # Show first 100 chars for brevity
    
    # Punctuation Removal
    translator = str.maketrans('', '', string.punctuation)
    content = content.translate(translator)
    logger.debug(f"Content after Punctuation Removal: {content[:100]}...")  # First 100 chars
    
    # Tokenization
    tokens = content.split()
    logger.debug(f"Tokenized Content: {tokens[:10]}...")  # Show first 10 tokens
    
    # Stopwords Removal
    tokens = [word for word in tokens if word not in stop_words]
    logger.debug(f"Content after Stopwords Removal: {tokens[:10]}...")  # First 10 tokens
    
    # Stemming (Optional)
    if apply_stemming:
        tokens = [stemmer.stem(word) for word in tokens]
        logger.debug(f"Content after Stemming: {tokens[:10]}...")  # First 10 tokens
    
    # Rejoin Tokens
    processed_content = ' '.join(tokens)
    logger.debug(f"Processed Content: {processed_content[:100]}...")  # First 100 chars
    
    # Final Check
    if not processed_content.strip():
        logger.error("ValueError: No valid content after preprocessing.")
        raise ValueError("No valid content after preprocessing.")
    
    return processed_content

def get_sentiment_label(prediction):
    """
    Maps a numerical or string prediction to a sentiment label.

    Args:
        prediction (int or str): The sentiment prediction.

    Returns:
        str: The corresponding sentiment label.
    """
    if isinstance(prediction, int):
        labels = {0: "negative", 1: "neutral", 2: "positive"}
        label = labels.get(prediction, "unknown")
    elif isinstance(prediction, str):
        labels = {"negative": "negative", "neutral": "neutral", "positive": "positive"}
        label = labels.get(prediction.lower(), "unknown")
    else:
        label = "unknown"
    
    logger.debug(f"Sentiment Label: {label}")
    return label
