import os
from werkzeug.utils import secure_filename
from utils.preprocess import preprocess_file_content, split_into_paragraphs
from services.sentiment_service import SentimentService
import logging
import PyPDF2

logger = logging.getLogger(__name__)

class UploadService:
    def __init__(self):
        self.allowed_extensions = {'txt', 'pdf'}
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.sentiment_service = SentimentService()

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def process_file(self, file):
        if not self.allowed_file(file.filename):
            logger.warning("Attempted to upload an unsupported file type.")
            raise ValueError("Unsupported file type. Please upload a .txt or .pdf file.")
        
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file.seek(0)

        if file_length > self.max_file_size:
            logger.warning(f"Uploaded file exceeds the maximum allowed size: {file_length} bytes.")
            raise ValueError("File size exceeds the maximum limit of 10MB.")

        filename = secure_filename(file.filename)
        logger.info(f"Processing file: {filename}")

        try:
            if filename.endswith('.txt'):
                content = file.read().decode('utf-8').strip()
            elif filename.endswith('.pdf'):
                content = self.extract_text_from_pdf(file)
            else:
                raise ValueError("Unsupported file format.")
        except UnicodeDecodeError as e:
            logger.error(f"Unicode decode error: {e}")
            raise ValueError("The file contains unsupported characters or encoding. Please upload a properly encoded file.")
        except Exception as e:
            logger.error(f"Error reading the file: {e}")
            raise ValueError("Error reading the file. Please ensure it's a valid text or PDF file.")

        if not content:
            logger.warning("File content is empty.")
            raise ValueError("The file is empty or does not contain valid text.")

        # Split content into paragraphs and analyze each
        try:
            paragraphs = split_into_paragraphs(content)
            sentiments = self.sentiment_service.analyze_sentiments(paragraphs)
            logger.info("Sentiment analysis completed.")
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            raise ValueError("Error during sentiment analysis.")

        logger.info(f"File processed successfully: {filename}")
        return filename, sentiments, paragraphs

    def extract_text_from_pdf(self, file):
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text.strip()

    def close(self):
        pass

