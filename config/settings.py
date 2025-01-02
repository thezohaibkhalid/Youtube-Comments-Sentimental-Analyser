import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
    INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB limit
    UPLOAD_EXTENSIONS = ['.txt', '.csv']
    UPLOAD_PATH = 'uploads'