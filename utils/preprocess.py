import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def preprocess_comment(comment, stopwords_english, stemmer):
    comment = comment.lower()
    comment = comment.translate(str.maketrans("", "", string.punctuation))
    comment = remove_stopwords(comment, stopwords_english)
    comment = stem_words(comment, stemmer)
    return comment

def remove_stopwords(comment, stopwords_english):
    comment_tokens = comment.split()
    return " ".join([word for word in comment_tokens if word not in stopwords_english])

def stem_words(comment, stemmer):
    comment_tokens = comment.split()
    return " ".join([stemmer.stem(word) for word in comment_tokens])

def get_sentiment_label(prediction):
    labels = {0: "negative", 1: "neutral", 2: "positive"}
    return labels.get(prediction, "unknown")
