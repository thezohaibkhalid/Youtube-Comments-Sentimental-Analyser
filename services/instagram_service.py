# services/instagram_service.py

import os
import time
from playwright.sync_api import sync_playwright
from utils.instagram_utils import extract_instagram_shortcode


class InstagramService:
    def __init__(self):
        self.username = os.getenv("INSTAGRAM_USERNAME")
        self.password = os.getenv("INSTAGRAM_PASSWORD")
        if not self.username or not self.password:
            raise ValueError("Instagram credentials not found in environment variables.")
        
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)  # Set headless=False for debugging
        self.context = self.browser.new_context(viewport={"width": 1920, "height": 1080})
        self.page = self.context.new_page()
        self._login()

    def _login(self):
        page = self.page
        page.goto("https://www.instagram.com/accounts/login/")
        page.wait_for_timeout(3000)  # Wait for the login page to load

        # Enter username
        page.fill("input[name='username']", self.username)

        # Enter password
        page.fill("input[name='password']", self.password)
        page.press("input[name='password']", "Enter")
        page.wait_for_timeout(5000)  # Wait for login to complete

        # Handle "Save Your Login Info?" popup
        try:
            page.locator("text=Not Now").click(timeout=3000)
        except:
            pass

        # Handle "Turn on Notifications" popup
        try:
            page.locator("text=Not Now").click(timeout=3000)
        except:
            pass

    def extract_instagram_shortcode(self, url):
        return extract_instagram_shortcode(url)

    def get_instagram_comments(self, shortcode, max_comments=100):
        page = self.page
        post_url = f"https://www.instagram.com/p/{shortcode}/"
        page.goto(post_url)
        page.wait_for_timeout(5000)  # Wait for the post page to load

        comments = set()
        last_height = None

        while len(comments) < max_comments:
            # Parse comments
            comment_elements = page.locator("//ul[@class='Mr508']/div/li/div/div/div/span")
            for i in range(comment_elements.count()):
                comment_text = comment_elements.nth(i).inner_text().strip()
                if comment_text:
                    comments.add(comment_text)
                    if len(comments) >= max_comments:
                        break

            # Scroll down to load more comments
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Wait for comments to load

            # Check if we've reached the end
            new_height = page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                break  # No more comments to load
            last_height = new_height

        return list(comments)[:max_comments]

    def close(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()
