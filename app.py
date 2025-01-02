# app.py

from flask import Flask, render_template
from config.settings import Config
from blueprints.analyze import analyze_bp  # Assuming you have this blueprint
from blueprints.youtube import youtube_bp
from blueprints.instagram import instagram_bp  # Assuming you have this blueprint
from blueprints.upload import upload_bp  # If you have this blueprint
from dotenv import load_dotenv
import os
import nltk
import logging
def create_app():

    load_dotenv()

    # Initialize NLTK data
    nltk.download("stopwords", quiet=True)

    # Initialize Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

        # Configure global logging
    logging.basicConfig(level=logging.DEBUG,   
                        format='%(asctime)s %(levelname)s %(name)s %(message)s',
                        handlers=[
                            logging.StreamHandler()   
                        ])
  

    # Register Blueprints
    app.register_blueprint(analyze_bp)
    app.register_blueprint(youtube_bp)
    app.register_blueprint(instagram_bp)
    app.register_blueprint(upload_bp)  # Register the upload blueprint if it exists

    # Home route
    @app.route("/")
    def home():
        return render_template("index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
