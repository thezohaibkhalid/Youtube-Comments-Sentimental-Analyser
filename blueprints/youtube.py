# blueprints/youtube.py

from flask import Blueprint, render_template, request, jsonify
from services.sentiment_service import SentimentService
from services.youtube_service import YouTubeService
from utils.youtube_utils import extract_youtube_video_id
import logging

youtube_bp = Blueprint('youtube', __name__)

@youtube_bp.route("/youtube", methods=["POST"])
def analyze_youtube():
    youtube_url = request.form.get("youtube_url")
    
    if not youtube_url:
        error_message = "No YouTube URL provided."
        return render_template("result.html", error=error_message)
    
    youtube_service = YouTubeService()
    sentiment_service = SentimentService()
    
    # Extract video ID
    video_id = extract_youtube_video_id(youtube_url)
    if not video_id:
        error_message = "Invalid YouTube URL."
        return render_template("result.html", error=error_message)
    
    # Fetch YouTube comments
    youtube_comments = youtube_service.get_youtube_comments(video_id)
    if not youtube_comments:
        return render_template(
            "result.html",
            youtube_sentiment={"message": "No comments found for this video."},
            youtube_url=youtube_url
        )
    
    # Analyze sentiments of YouTube comments
    youtube_sentiment = sentiment_service.analyze_sentiments(youtube_comments)
    
    return render_template(
        "result.html",
        youtube_sentiment=youtube_sentiment,
        youtube_comments=youtube_comments,
        youtube_url=youtube_url
    )



    # blueprints/youtube.py

from flask import Blueprint, render_template, request, jsonify
from services.sentiment_service import SentimentService
from services.youtube_service import YouTubeService
from utils.youtube_utils import extract_youtube_video_id
import logging

youtube_bp = Blueprint('youtube', __name__)

@youtube_bp.route("/youtube", methods=["POST"])
def analyze_youtube():
    youtube_url = request.form.get("youtube_url")
    
    if not youtube_url:
        error_message = "No YouTube URL provided."
        return render_template("result.html", error=error_message), 400
    
    youtube_service = YouTubeService()
    sentiment_service = SentimentService()
    
    # Extract video ID
    video_id = extract_youtube_video_id(youtube_url)
    if not video_id:
        error_message = "Invalid YouTube URL."
        return render_template("result.html", error=error_message), 400
    
    # Fetch YouTube comments
    youtube_comments = youtube_service.get_youtube_comments(video_id)
    if not youtube_comments:
        return render_template(
            "result.html",
            youtube_sentiment={"message": "No comments found for this video."},
            youtube_url=youtube_url
        )
    
    # Analyze sentiments of YouTube comments
    youtube_sentiment = sentiment_service.analyze_sentiments(youtube_comments)
    
    return render_template(
        "result.html",
        youtube_sentiment=youtube_sentiment,
        youtube_comments=youtube_comments,
        youtube_url=youtube_url
    )
