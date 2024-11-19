import random
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from sqlalchemy import select
import logging

from app.app import create_app, db
from backend.data.models import AllCoins

logger = logging.getLogger(__name__)


class WebsiteError(Exception):
    pass


class BaseScrapper:
    def __init__(self, config):
        self.config = config

    def scrap(self):
        raise NotImplementedError

    def update_all_coins(self, coins):
        if not coins:
            return

        app = create_app(self.config)
        with app.app_context():
            existing_all_coins = {
                coin.id for coin in db.session.execute(select(AllCoins)).scalars().all()
            }
            to_update = []

            for id, coin in coins.items():
                if (
                    id in existing_all_coins
                    or id.lower() in existing_all_coins
                    or id.upper() in existing_all_coins
                    or id.capitalize() in existing_all_coins
                ):
                    continue
                logger.info(f"Found coin: {id}")
                to_update.append(
                    AllCoins(
                        id=coin.id,
                        symbol=coin.symbol,
                        name=coin.name,
                        source=coin.source,
                        is_shit=False,
                    )
                )
            if to_update:
                db.session.bulk_save_objects(to_update)
                db.session.commit()

    def fetch_data(self, config):
        tries = 3
        for i in range(0, tries):
            time.sleep(4)
            response = requests.get(
                url=config["url"], headers=config["headers"], timeout=config["timeout"]
            )
            logger.info(f"Response: {response.status_code}")
            response.raise_for_status()
            return response


class scrap_website_driver:
    def __init__(self, website):
        self.website = website

    def __enter__(self):
        chrome_options = Options()
        chrome_options.add_argument(f'user-agent={self.user_agent}')
        # chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.website)
        logger.info(f"Open: {self.website}")
        return self.driver

    def __exit__(self, type, value, traceback):
        self.driver.quit()

    @property
    def user_agent(self):
        random.choice(
            [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
            ]
        )


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
