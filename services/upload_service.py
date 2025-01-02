# services/upload_service.py

import os
from werkzeug.utils import secure_filename
from utils.preprocess import preprocess_text
from services.sentiment_service import SentimentService
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UploadService:
    def __init__(self):
        self.allowed_extensions = {'txt', 'csv'}
        self.max_file_size = 5 * 1024 * 1024  # 5MB
        self.sentiment_service = SentimentService()

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

def process_file(self, file):
    if not self.allowed_file(file.filename):
        logger.warning("Attempted to upload an unsupported file type.")
        raise ValueError("Unsupported file type. Please upload a .txt or .csv file.")
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0)
    
    if file_length > self.max_file_size:
        logger.warning("Uploaded file exceeds the maximum allowed size.")
        raise ValueError("File size exceeds the maximum limit of 5MB.")
    
    filename = secure_filename(file.filename)
    logger.info(f"Processing file: {filename}")
    
    try:
        if filename.endswith('.txt'):
            content = file.read().decode('utf-8')
            lines = content.splitlines()
        elif filename.endswith('.csv'):
            import csv
            content = file.read().decode('utf-8')
            reader = csv.reader(content.splitlines())
            lines = [row[0] for row in reader if row]  # Assuming text is in the first column
        else:
            raise ValueError("Unsupported file format.")
    except UnicodeDecodeError as e:
        logger.error(f"Error decoding the file: {e}")
        raise ValueError("Error reading the file. Please ensure it's a valid text or CSV file with proper encoding.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise ValueError("Error reading the file. Please ensure it's a valid text or CSV file.")

    # Extract sample text (first 5 lines) and preprocess
    sample_text = preprocess_text(lines[:5], apply_stemming=False)  # Disable stemming for consistency
    logger.info("Sample text extracted and preprocessed.")

    # Ensure that sentiment analysis only processes valid lines
    valid_lines = [line for line in lines if line.strip()]  # Remove empty lines
    if not valid_lines:
        raise ValueError("No valid text found for sentiment analysis.")

    # Perform sentiment analysis
    sentiments = self.sentiment_service.analyze_sentiments(valid_lines)
    logger.info("Sentiment analysis completed.")

    logger.info(f"File processed successfully: {filename}")
    return filename, sentiments, sample_text

    def close(self):
        # Removed the call to self.sentiment_service.close() to prevent AttributeError
        pass
