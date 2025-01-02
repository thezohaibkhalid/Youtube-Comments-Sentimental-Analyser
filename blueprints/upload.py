from flask import Blueprint, render_template, request, jsonify
from services.sentiment_service import SentimentService
from services.upload_service import UploadService
import os

upload_bp = Blueprint('upload', __name__)

@upload_bp.route("/upload", methods=["POST"])
def analyze_upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request."}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading."}), 400
    
    # Initialize the sentiment service
    sentiment_service = SentimentService()
    upload_service = UploadService()
    
    try:
        # Process the uploaded file
        filename, sentiments, sample_text = upload_service.process_file(file)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred while processing the file."}), 500
    finally:
        upload_service.close()  # Now, this does nothing as close() is pass
    
    # Prepare the data for rendering
    file_sentiment = {
        "filename": filename,
        "sentiments": sentiments,
        "sample_text": sample_text
    }
    
    return render_template(
        "result.html",
        file_sentiment=file_sentiment
    )
