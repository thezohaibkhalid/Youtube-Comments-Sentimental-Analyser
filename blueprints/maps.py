from flask import Blueprint, request, render_template, redirect, url_for, flash
from services.scraper_service import scrape_and_analyze
import asyncio
import logging

maps_bp = Blueprint('maps', __name__)
logger = logging.getLogger(__name__)

@maps_bp.route('/analyze_maps', methods=['POST'])
def analyze_maps():
    googlemaps_url = request.form.get('googlemaps_url')
    
    if not googlemaps_url:
        flash('No Google Maps URL provided.', 'error')
        return redirect(url_for('home'))
    
    try:
        result = asyncio.run(scrape_and_analyze(googlemaps_url))
        
        return render_template(
            'result.html',
            googlemaps_url=googlemaps_url,
            place_name=result['title'],
            total_reviews=result['total_reviews'],
            sentiment_percentages=result['sentiment_percentages'],
            reviews=result['reviews'],
        )
    
    except Exception as e:
        logger.error(f"Error during Google Maps sentiment analysis: {e}")
        flash('An error occurred while processing your request.', 'error')
        return redirect(url_for('home'))

@maps_bp.route('/maps', methods=['POST'])
def maps_redirect():
    return analyze_maps()

