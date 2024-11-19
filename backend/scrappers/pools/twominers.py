from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from app.app import get_logger
from backend.data.models import AllCoins
from backend.utils.scrappers import BaseScrapper, scrap_website_driver

logger = get_logger()


class TwoMiners(BaseScrapper):
    def run(self):
        scrap_config = self.config.scrappers[self.name]
        if not scrap_config["enabled"]:
            return

        with scrap_website_driver(scrap_config["url"]) as driver:
            name_elements = WebDriverWait(driver, scrap_config["timeout"]).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, scrap_config["XPATHS"][0])
                )
            )
            new_coins = {}
            for name in name_elements:
                coin_name = name.get_property("title")
                breakpoint()
                new_coins[coin_name] = AllCoins(
                    id=coin_name,
                    symbol="",
                    name=coin_name,
                    source=self.name,
                    is_shit=False,
                )

        self.update_all_coins(new_coins)
