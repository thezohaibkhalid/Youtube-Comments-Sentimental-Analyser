from flask import Blueprint, render_template, request, jsonify
from services.sentiment_service import SentimentService

analyze_bp = Blueprint('analyze', __name__)

@analyze_bp.route("/analyze", methods=["POST"])
def analyze():
    comment = request.form.get("comment")
    
    if not comment:
        return jsonify({"error": "No comment provided."}), 400
    
    sentiment_service = SentimentService()
    
    # Analyze the main comment
    processed_comment = sentiment_service.preprocess_comment(comment)
    sentiment = sentiment_service.get_sentiment(processed_comment)
    
    return render_template(
        "result.html",
        comment=comment,
        sentiment=sentiment
    )
