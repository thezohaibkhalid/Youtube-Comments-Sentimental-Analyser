from flask import Blueprint, request, render_template, redirect, url_for, flash
from utils.preprocess import preprocess_comment
from services.maps_service import (
    extract_place_id,
    fetch_google_maps_reviews,
    analyze_sentiments,
)

import logging

maps_bp = Blueprint('maps', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@maps_bp.route('/maps', methods=['POST'])
def analyze_maps():
    googlemaps_url = request.form.get('googlemaps_url')
    
    if not googlemaps_url:
        flash('No Google Maps URL provided.', 'error')
        return redirect(url_for('index'))
    
    try:
        place_id = extract_place_id(googlemaps_url)
        if not place_id:
            flash('Invalid Google Maps embed URL.', 'error')
            return redirect(url_for('index'))
        
        reviews = fetch_google_maps_reviews(place_id)
        if not reviews:
            flash('No reviews found for the provided location.', 'info')
            return redirect(url_for('index'))
        
        preprocessed_reviews = [preprocess_comment(review['text'], set(), None, False) for review in reviews]
        
        sentiment_results = analyze_sentiments(preprocessed_reviews)
        
        total_reviews = len(sentiment_results)
        positive = sum(1 for sentiment in sentiment_results if sentiment == 'positive')
        neutral = sum(1 for sentiment in sentiment_results if sentiment == 'neutral')
        negative = sum(1 for sentiment in sentiment_results if sentiment == 'negative')
        
        sentiment_percentages = {
            'positive': round((positive / total_reviews) * 100, 2),
            'neutral': round((neutral / total_reviews) * 100, 2),
            'negative': round((negative / total_reviews) * 100, 2),
        }
        
        return render_template(
            'maps_result.html',
            googlemaps_url=googlemaps_url,
            total_reviews=total_reviews,
            sentiment_percentages=sentiment_percentages,
            reviews=reviews[:10],  # Show top 10 reviews
        )
    
    except Exception as e:
        logger.error(f"Error during Google Maps sentiment analysis: {e}")
        flash('An error occurred while processing your request.', 'error')
        return redirect(url_for('index'))
