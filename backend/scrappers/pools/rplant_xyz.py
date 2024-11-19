import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from app.app import get_logger
from backend.data.models import AllCoins
from backend.utils.scrappers import BaseScrapper, scrap_website_driver

logger = get_logger()


class Rplant(BaseScrapper):
    def run(self):
        scrap_config = self.config.scrappers[self.name]
        if not scrap_config["enabled"]:
            return

        with scrap_website_driver(scrap_config["url"]) as driver:
            coins_page = scrap_config["XPATHS"][0]

            WebDriverWait(driver, scrap_config["timeout"]).until(
                EC.presence_of_element_located((By.XPATH, coins_page))
            )
            time.sleep(4)
            name_elements = driver.find_elements(By.XPATH, scrap_config["XPATHS"][1])
            name_elements = [
                td for td in name_elements if "sorting_1" in td.get_attribute("class")
            ]
            new_coins = {}
            for name in name_elements:
                new_coins[name.text] = AllCoins(
                    id=name.text,
                    symbol="",
                    name=name.text,
                    source=self.name,
                    is_shit=False,
                )
        self.update_all_coins(new_coins)
