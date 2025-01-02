# services/instagram_service.py

import os
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from utils.instagram_utils import extract_instagram_shortcode
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        try:
            logger.info("Navigating to Instagram login page.")
            page.goto("https://www.instagram.com/accounts/login/", timeout=60000)
            page.wait_for_selector("input[name='username']", timeout=10000)
            logger.info("Login page loaded.")

            # Enter username
            page.fill("input[name='username']", self.username)
            logger.info("Entered username.")

            # Enter password
            page.fill("input[name='password']", self.password)
            logger.info("Entered password.")

            # Submit the login form
            page.press("input[name='password']", "Enter")
            logger.info("Submitted login form.")

            # Wait for navigation after login
            page.wait_for_selector("nav", timeout=15000)  # Wait for the navigation bar to appear
            logger.info("Login successful.")

            # Handle "Save Your Login Info?" popup
            try:
                save_info_btn = page.locator("button:has-text('Not Now')")
                if save_info_btn.is_visible():
                    save_info_btn.click()
                    logger.info("Clicked 'Not Now' on 'Save Your Login Info?' popup.")
                    page.wait_for_timeout(3000)
            except PlaywrightTimeoutError:
                logger.warning("'Save Your Login Info?' popup did not appear.")

            # Handle "Turn on Notifications" popup
            try:
                turn_on_notif_btn = page.locator("button:has-text('Not Now')")
                if turn_on_notif_btn.is_visible():
                    turn_on_notif_btn.click()
                    logger.info("Clicked 'Not Now' on 'Turn on Notifications' popup.")
                    page.wait_for_timeout(3000)
            except PlaywrightTimeoutError:
                logger.warning("'Turn on Notifications' popup did not appear.")

        except PlaywrightTimeoutError as e:
            logger.error(f"Timeout during login process: {e}")
            self.close()
            raise
        except Exception as e:
            logger.error(f"An error occurred during login: {e}")
            self.close()
            raise

    def extract_instagram_shortcode(self, url):
        return extract_instagram_shortcode(url)

    def get_instagram_comments(self, shortcode, max_comments=100):
        page = self.page
        post_url = f"https://www.instagram.com/p/{shortcode}/"
        try:
            logger.info(f"Navigating to Instagram post: {post_url}")
            page.goto(post_url, timeout=60000)
            page.wait_for_selector("article", timeout=15000)
            logger.info("Post page loaded.")

            # Click on the comments section to ensure comments are loaded
            try:
                comments_button = page.locator("span:has-text('comments')").first
                if comments_button.is_visible():
                    comments_button.click()
                    logger.info("Clicked on comments section.")
                    page.wait_for_timeout(3000)
            except PlaywrightTimeoutError:
                logger.warning("Comments button not found or not clickable.")

            comments = set()
            last_height = page.evaluate("document.body.scrollHeight")
            scroll_attempts = 0
            max_scroll_attempts = 10

            while len(comments) < max_comments and scroll_attempts < max_scroll_attempts:
                # Extract comment elements
                comment_elements = page.locator("ul.Mr508 li div div div span")
                count = comment_elements.count()
                logger.info(f"Found {count} comments on the current view.")

                for i in range(count):
                    comment_text = comment_elements.nth(i).inner_text().strip()
                    if comment_text and comment_text not in comments:
                        comments.add(comment_text)
                        if len(comments) >= max_comments:
                            logger.info(f"Reached desired number of comments: {max_comments}")
                            break

                # Scroll down to load more comments
                page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)  # Wait for comments to load

                # Check if new comments have been loaded
                new_height = page.evaluate("document.body.scrollHeight")
                if new_height == last_height:
                    scroll_attempts += 1
                    logger.info(f"No new comments loaded. Scroll attempt {scroll_attempts}/{max_scroll_attempts}.")
                else:
                    last_height = new_height
                    scroll_attempts = 0  # Reset scroll attempts if new comments are loaded

            logger.info(f"Total comments fetched: {len(comments)}")
            return list(comments)[:max_comments]

        except PlaywrightTimeoutError as e:
            logger.error(f"Timeout while fetching comments: {e}")
            return []
        except Exception as e:
            logger.error(f"An error occurred while fetching Instagram comments: {e}")
            return []

    def close(self):
        try:
            self.context.close()
            self.browser.close()
            self.playwright.stop()
            logger.info("Closed Playwright browser and context.")
        except Exception as e:
            logger.error(f"An error occurred while closing Playwright: {e}")
