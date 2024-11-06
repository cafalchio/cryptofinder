import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


class WebsiteError(Exception):
    pass


class scrap_website_driver:
    def __init__(self, website):
        self.website = website

    def __enter__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.website)
        logger.info(f"Open: {self.website}")
        return self.driver

    def __exit__(self, type, value, traceback):
        self.driver.quit()


class scrap_website_soup:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    def __init__(self, website):
        self.website = website

    def __enter__(self):
        page = requests.get(self.website, headers=self.headers)
        if page.status_code != 200:
            raise WebsiteError(
                f"Failed to retrieve website. Status code: {page.status_code}"
            )
        logger.info(f"Open: {self.website}")
        return BeautifulSoup(page.text, "html.parser")

    def __exit__(self, type, value, traceback):
        pass
