import random
import time
from requests import request
from selenium import webdriver
from bs4 import BeautifulSoup
from sqlalchemy import select
import logging

from app.app import create_app, db
from backend.data.models import AllCoins

logger = logging.getLogger(__name__)


class WebsiteError(Exception):
    pass


class ScrapperError(Exception):
    pass


def prGreen(skk, end=None):
    print("\033[92m {}\033[00m".format(skk), end=end)


class BaseScrapper:
    name = NotImplementedError

    def __init__(self, config):
        self.config = config
        self.name = self.__class__.__name__

    def run(self):
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
                prGreen("Ok", end="...")
                print(f"{len(to_update)} new")
                db.session.bulk_save_objects(to_update)
                db.session.commit()
                to_update = []
            else:
                prGreen("Ok")

    def fetch_data(self, config):
        tries = 3
        for i in range(0, tries):
            time.sleep(4)
            response = request(
                method=config["method"],
                url=config["url"],
                headers=config["headers"],
                timeout=config["timeout"],
                data=config["payload"],
            )
            logger.info(f"Response: {response.status_code}")
            response.raise_for_status()
            return response


class scrap_website_driver:
    def __init__(self, website):
        self.website = website

    def __enter__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run without GUI
        # Overcome limited resource problems
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")  # Bypass OS security model
        options.add_argument("--disable-gpu")  # Applicable for headless mode

        selenium_server_url = "http://192.168.193.161:4444/wd/hub"

        # Initialize the WebDriver
        self.driver = webdriver.Remote(
            command_executor=selenium_server_url, options=options
        )
        # self.driver = driver = webdriver.Chrome(service=Service(
        #     ChromeDriverManager().install()), options=chrome_options)
        self.driver.get(self.website)
        logger.info(f"Open: {self.website}")
        return self.driver

    def __exit__(self, type, value, traceback):
        self.driver.quit()

    @property
    def user_agent(self):
        random.choice(
            [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
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
