import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from app.app import get_logger
from backend.data.models import AllCoins
from backend.utils.scrappers import BaseScrapper, scrap_website_driver

logger = get_logger()


class F2pool(BaseScrapper):
    def run(self):
        scrap_config = self.config.scrappers["f2pool"]
        if not scrap_config["enabled"]:
            return

        with scrap_website_driver(scrap_config["url"]) as driver:
            name_elements = scrap_config["XPATHS"][0]
            WebDriverWait(driver, scrap_config["timeout"]).until(EC.presence_of_element_located((By.XPATH, name_elements)))
            time.sleep(2)
            breakpoint()
            new_coins = {}
            for name in name_elements:
                breakpoint()

                new_coins[name.title] = AllCoins(
                    id=name.title,
                    symbol=name.text,
                    name=name.title,
                    source="f2pool",
                    is_shit=False,
                )
        self.update_all_coins(new_coins)
