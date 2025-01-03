import re
import logging
import os
import requests
from utils.preprocess import preprocess_comment
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# nltk.download('vader_lexicon')

logger = logging.getLogger(__name__)

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

if not GOOGLE_MAPS_API_KEY:
    logger.error("Google Maps API key not found. Please set the GOOGLE_MAPS_API_KEY environment variable.")
    raise ValueError("Google Maps API key not found. Please set the GOOGLE_MAPS_API_KEY environment variable.")

def extract_place_id(url):
    try:
        if 'maps.app.goo.gl' in url:
            # Handle short URL format
            response = requests.get(url, allow_redirects=False)
            if response.status_code == 302:
                long_url = response.headers['Location']
                match = re.search(r'!1s([\w\-]+)', long_url)
                if match:
                    return match.group(1)
        else:
            # Handle embed URL format
            match = re.search(r'!1s([\w\-]+)', url)
            if match:
                return match.group(1)
        
        logger.error("Place ID not found in the URL.")
        return None
    except Exception as e:
        logger.error(f"Error extracting Place ID: {e}")
        return None

def get_place_details(place_id):
    try:
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'place_id': place_id,
            'fields': 'name,rating,review',
            'key': GOOGLE_MAPS_API_KEY
        }
        response = requests.get(url, params=params)
        data = response.json()
        if data.get('status') == 'OK':
            return data['result']
        else:
            logger.error(f"Place Details API error: {data.get('status')}")
            return None
    except Exception as e:
        logger.error(f"Error getting place details: {e}")
        return None

def fetch_google_maps_reviews(place_id):
    place_details = get_place_details(place_id)
    if place_details:
        reviews = place_details.get('reviews', [])
        formatted_reviews = [{'author': review.get('author_name'), 'rating': review.get('rating'), 'text': review.get('text')} for review in reviews]
        logger.info(f"Fetched {len(formatted_reviews)} reviews.")
        return formatted_reviews, place_details.get('name'), place_details.get('rating')
    return [], None, None

def analyze_sentiments(reviews):
    try:
        sia = SentimentIntensityAnalyzer()
        sentiments = []
        for review in reviews:
            score = sia.polarity_scores(review['text'])
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

