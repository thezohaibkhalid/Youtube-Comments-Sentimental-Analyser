import re
import logging
import os
import requests
from utils.preprocess import preprocess_comment
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Ensure NLTK data is downloaded
nltk.download('vader_lexicon')

logger = logging.getLogger(__name__)

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

if not GOOGLE_MAPS_API_KEY:
    logger.error("Google Maps API key not found. Please set the GOOGLE_MAPS_API_KEY environment variable.")
    raise ValueError("Google Maps API key not found. Please set the GOOGLE_MAPS_API_KEY environment variable.")

def extract_place_id(embed_url):
    try:
        match = re.search(r'2s([^!]+)', embed_url)
        if match:
            place_name = match.group(1).replace('%20', ' ')
            logger.info(f"Extracted place name: {place_name}")
            place_id = get_place_id(place_name)
            return place_id
        else:
            logger.error("Place name not found in the embed URL.")
            return None
    except Exception as e:
        logger.error(f"Error extracting Place ID: {e}")
        return None

def get_place_id(place_name):
    try:
        url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        params = {
            'input': place_name,
            'inputtype': 'textquery',
            'fields': 'place_id',
            'key': GOOGLE_MAPS_API_KEY
        }
        response = requests.get(url, params=params)
        data = response.json()
        if data.get('status') == 'OK' and data.get('candidates'):
            place_id = data['candidates'][0]['place_id']
            logger.info(f"Obtained Place ID: {place_id}")
            return place_id
        else:
            logger.error(f"Places API error: {data.get('status')}")
            return None
    except Exception as e:
        logger.error(f"Error getting Place ID: {e}")
        return None

def fetch_google_maps_reviews(place_id):
    try:
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'place_id': place_id,
            'fields': 'review',
            'key': GOOGLE_MAPS_API_KEY
        }
        response = requests.get(url, params=params)
        data = response.json()
        if data.get('status') == 'OK':
            reviews = data['result'].get('reviews', [])
            formatted_reviews = [{'author': review.get('author_name'), 'rating': review.get('rating'), 'text': review.get('text')} for review in reviews]
            logger.info(f"Fetched {len(formatted_reviews)} reviews.")
            return formatted_reviews
        else:
            logger.error(f"Place Details API error: {data.get('status')}")
            return []
    except Exception as e:
        logger.error(f"Error fetching reviews: {e}")
        return []

def analyze_sentiments(reviews):
    try:
        sia = SentimentIntensityAnalyzer()
        sentiments = []
        for review in reviews:
            score = sia.polarity_scores(review)
            compound = score['compound']
            if compound >= 0.05:
                sentiments.append('positive')
            elif compound <= -0.05:
                sentiments.append('negative')
            else:
                sentiments.append('neutral')
        logger.info(f"Sentiment analysis completed for {len(sentiments)} reviews.")
        return sentiments
    except Exception as e:
        logger.error(f"Error during sentiment analysis: {e}")
        return []
