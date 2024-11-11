from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from app.app import get_logger
from backend.data.models import AllCoins
from backend.utils.scrappers import BaseScrapper, scrap_website_driver
from selenium.common.exceptions import TimeoutException

logger = get_logger()


class MiningPoolStats(BaseScrapper):
    def run(self):
        scrap_config = self.config.scrappers["miningpoolstats"]
        with scrap_website_driver(scrap_config["url"]) as driver:
            try:
                button = WebDriverWait(driver, scrap_config["timeout"]).until(
                    EC.element_to_be_clickable((By.XPATH, scrap_config["XPATHS"][0]))
                )
                button.click()
            except TimeoutException:
                pass

            WebDriverWait(driver, scrap_config["timeout"]).until(
                EC.presence_of_element_located((By.XPATH, scrap_config["XPATHS"][1]))
            )

            name_elements = driver.find_elements(By.XPATH, scrap_config["XPATHS"][2])
            symbol_elements = driver.find_elements(By.XPATH, scrap_config["XPATHS"][3])
            new_coins = {}
            for name, symbol in zip(name_elements, symbol_elements):
                new_coins[name.text] = AllCoins(
                    id=name.text,
                    symbol=symbol.text,
                    name=name.text,
                    source="miningpool",
                    is_shit=False,
                )
        self.update_all_coins(new_coins)
