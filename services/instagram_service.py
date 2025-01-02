# services/instagram_service.py

import instaloader
import os
from utils.instagram_utils import extract_instagram_shortcode
from config.settings import Config
class InstagramService:
    def __init__(self):
        self.loader = instaloader.Instaloader()
        self.username = Config.INSTAGRAM_USERNAME
        self.password = Config.INSTAGRAM_PASSWORD
        if self.username and self.password:
            try:
                self.loader.login(self.username, self.password)
            except Exception as e:
                print(f"Failed to login to Instagram: {e}")
        else:
            print("Instagram credentials not found. Proceeding without login.")

    def extract_instagram_shortcode(self, url):
        return extract_instagram_shortcode(url)

    def get_instagram_comments(self, shortcode, max_comments=100):
        comments = []
        try:
            post = instaloader.Post.from_shortcode(self.loader.context, shortcode)
            for comment in post.get_comments():
                comments.append(comment.text)
                if len(comments) >= max_comments:
                    break
        except Exception as e:
            print(f"An error occurred while fetching Instagram comments: {e}")
        return comments
