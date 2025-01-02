from flask import Flask, render_template
from config.settings import Config
from blueprints.analyze import analyze_bp
from blueprints.youtube import youtube_bp
from blueprints.instagram import instagram_bp
from dotenv import load_dotenv
import os

import nltk

nltk.download("stopwords")

def create_app():
    # Load environment variables
    load_dotenv()

    # Initialize Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register Blueprints
    app.register_blueprint(analyze_bp)
    app.register_blueprint(youtube_bp)
    app.register_blueprint(instagram_bp)

    # Home route
    @app.route("/")
    def home():
        return render_template("index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
