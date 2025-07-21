import os
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class SmashKartsBgBot:
    def __init__(self):
        self.driver = None
        self.bot_running = False
        self.bot_thread = None

    def setup_browser_bg(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--user-data-dir=/tmp/bot_profile")
        chrome_options.add_argument("--remote-debugging-port=9223")
        chrome_options.add_argument("--window-size=1280,720")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--display=:99")
        self.driver = webdriver.Chrome(options=chrome_options)

    def navigate_and_setup(self, url="https://smashkarts.io/"):
        self.driver.get(url)
        time.sleep(5)

    def bot_cycle(self):
        body = self.driver.find_element(By.TAG_NAME, "body")
        actions = ActionChains(self.driver)
        while self.bot_running:
            try:
                actions.key_down(Keys.ARROW_UP).perform()
                time.sleep(2)
                actions.key_up(Keys.ARROW_UP).perform()
                actions.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                time.sleep(0.5)
            except Exception:
                break

    def start_bot(self):
        if not self.bot_running:
            self.bot_running = True
            self.bot_thread = threading.Thread(target=self.bot_cycle, daemon=True)
            self.bot_thread.start()
            return True
        return False

    def stop_bot(self):
        if self.bot_running:
            self.bot_running = False
            if self.bot_thread:
                self.bot_thread.join(timeout=2)
            return True
        return False

# Singleton instance for Flask app
bot_instance = SmashKartsBgBot() 