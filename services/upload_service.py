# services/upload_service.py

import os
from werkzeug.utils import secure_filename
from utils.preprocess import preprocess_file_content
from services.sentiment_service import SentimentService
import logging

# Define the logger for this module
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
                content = file.read().decode('utf-8').strip()
            elif filename.endswith('.csv'):
                import csv
                content = file.read().decode('utf-8').strip()
                reader = csv.reader(content.splitlines())
                # Assuming text is in the first column
                content = ' '.join([row[0] for row in reader if row])
            else:
                raise ValueError("Unsupported file format.")
        except UnicodeDecodeError as e:
            logger.error(f"Unicode decode error: {e}")
            raise ValueError("File contains unsupported characters or encoding.")
        except Exception as e:
            logger.error(f"Error reading the file: {e}")
            raise ValueError("Error reading the file. Please ensure it's a valid text or CSV file.")

        # Preprocess the entire content for sentiment analysis
        try:
            preprocessed_content = preprocess_file_content(content, apply_stemming=False)
            logger.info("File content preprocessed successfully.")
        except (TypeError, ValueError) as e:
            logger.error(f"Preprocessing error: {e}")
            raise ValueError(f"Preprocessing error: {e}")

        # Perform sentiment analysis on the entire content
        try:
            sentiments = self.sentiment_service.analyze_sentiments([preprocessed_content])  # Pass as a list with one item
            logger.info("Sentiment analysis completed.")
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            raise ValueError("Error during sentiment analysis.")

        # Prepare a sample text (e.g., first 500 characters)
        sample_text = preprocessed_content[:500] + '...' if len(preprocessed_content) > 500 else preprocessed_content
        logger.info("Sample text prepared.")

        logger.info(f"File processed successfully: {filename}")
        return filename, sentiments, sample_text

    def close(self):
        # Removed the call to self.sentiment_service.close() to prevent AttributeError
        pass
