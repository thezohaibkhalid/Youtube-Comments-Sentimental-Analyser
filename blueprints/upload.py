import logging
from flask import Blueprint, render_template, request
from services.upload_service import UploadService

# Define the logger for this module
logger = logging.getLogger(__name__)

upload_bp = Blueprint('upload', __name__)

@upload_bp.route("/upload", methods=["POST"])
def analyze_upload():
    if 'file' not in request.files:
        error_message = "No file part in the request."
        logger.error(error_message)
        return render_template("result.html", error=error_message), 400

    file = request.files['file']

    if file.filename == '':
        error_message = "No file selected for uploading."
        logger.error(error_message)
        return render_template("result.html", error=error_message), 400

    upload_service = UploadService()
    
    try:
        filename, sentiments, sample_text = upload_service.process_file(file)
    except ValueError as ve:
        error_message = str(ve)
        logger.error(f"ValueError: {error_message}")
        return render_template("result.html", error=error_message), 400
    except Exception as e:
        error_message = "An error occurred while processing the file."
        logger.error(f"Exception: {str(e)}")
        return render_template("result.html", error=error_message), 500
    
    # Return successful result
    file_sentiment = {
        "filename": filename,
        "sentiments": sentiments,
        "sample_text": sample_text
    }

    return render_template("result.html", file_sentiment=file_sentiment)

