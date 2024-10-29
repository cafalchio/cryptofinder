import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import logging
import time

logger = logging.getLogger(__name__)


class WebsiteError(Exception):
    pass


class scrap_website_driver:
    def __init__(self, website):
        self.website = website

    def __enter__(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.website)
        logger.info(f"Open: {self.website}")
        return self.driver

    def __exit__(self, type, value, traceback):
        self.driver.quit()


class scrap_website_soup:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }

    def __init__(self, website):
        self.website = website

    def __enter__(self):
        page = requests.get(self.website, headers=self.headers)
        if page.status_code != 200:
            raise WebsiteError(
                f"Failed to retrieve website. Status code: {page.status_code}")
        logger.info(f"Open: {self.website}")
        return BeautifulSoup(page.text, 'html.parser')

    def __exit__(self, type, value, traceback):
        pass
