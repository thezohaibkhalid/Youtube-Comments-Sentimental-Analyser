# services/instagram_service.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os
from utils.instagram_utils import extract_instagram_shortcode
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class InstagramService:
    def __init__(self):
        self.username = os.getenv("INSTAGRAM_USERNAME")
        self.password = os.getenv("INSTAGRAM_PASSWORD")
        if not self.username or not self.password:
            raise ValueError("Instagram credentials not found in environment variables.")
        self.driver = self._init_driver()
        self._login()

    def _init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        return driver

    def _login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)  # Wait for the login page to load

        # Enter username
        username_input = driver.find_element(By.NAME, "username")
        username_input.send_keys(self.username)

        # Enter password
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)

        time.sleep(5)  # Wait for login to complete

        # Handle "Save Your Login Info?" popup
        try:
            not_now_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
            not_now_button.click()
            time.sleep(3)
        except NoSuchElementException:
            pass

        # Handle "Turn on Notifications" popup
        try:
            not_now_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
            not_now_button.click()
            time.sleep(3)
        except NoSuchElementException:
            pass

    def extract_instagram_shortcode(self, url):
        return extract_instagram_shortcode(url)

    def get_instagram_comments(self, shortcode, max_comments=100):
        driver = self.driver
        post_url = f"https://www.instagram.com/p/{shortcode}/"
        driver.get(post_url)
        time.sleep(5)  # Wait for the post page to load

        comments = []
        last_height = driver.execute_script("return document.body.scrollHeight")

        while len(comments) < max_comments:
            # Scroll down to load more comments
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Wait for comments to load

            # Parse comments
            comment_elements = driver.find_elements(By.XPATH, "//ul[@class='Mr508']/div/li/div/div/div/span")
            for elem in comment_elements:
                comment_text = elem.text.strip()
                if comment_text and comment_text not in comments:
                    comments.append(comment_text)
                    if len(comments) >= max_comments:
                        break

            # Check if we've reached the end
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # No more comments to load
            last_height = new_height

        return comments[:max_comments]

    def close(self):
        self.driver.quit()
