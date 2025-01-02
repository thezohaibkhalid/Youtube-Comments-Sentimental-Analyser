from flask import Blueprint, render_template, request, jsonify
from services.sentiment_service import SentimentService
from services.instagram_service import InstagramService

instagram_bp = Blueprint('instagram', __name__)

@instagram_bp.route("/instagram", methods=["POST"])
def analyze_instagram():
    instagram_url = request.form.get("instagram_url")
    
    if not instagram_url:
        return jsonify({"error": "No Instagram URL provided."}), 400
    
    instagram_service = InstagramService()
    sentiment_service = SentimentService()
    
    # Extract shortcode
    shortcode = instagram_service.extract_instagram_shortcode(instagram_url)
    if not shortcode:
        return jsonify({"error": "Invalid Instagram URL."}), 400
    
    # Fetch Instagram comments
    instagram_comments = instagram_service.get_instagram_comments(shortcode)
    if not instagram_comments:
        return render_template(
            "result.html",
            instagram_sentiment={"message": "No comments found for this post."},
            instagram_url=instagram_url
        )
    
    # Analyze sentiments of Instagram comments
    instagram_sentiment = sentiment_service.analyze_sentiments(instagram_comments)
    
    return render_template(
        "result.html",
        instagram_sentiment=instagram_sentiment,
        instagram_comments=instagram_comments,
        instagram_url=instagram_url
    )