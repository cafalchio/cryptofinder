from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

from backend.data.models import AllCoins
from backend.scrappers.run_scrappers import update_all_coins
from backend.utils.scrappers import scrap_website_driver

logger = logging.getLogger(__name__)


def mining_pool_stats():
    new_coins = {}
    with scrap_website_driver("https://miningpoolstats.stream/newcoins") as driver:
        consent_button = "//button[@aria-label='Consent']"
        coins_page = "//*[@id='mainpage']"

        button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, consent_button))
        )
        logger.info(button)
        time.sleep(5)
        button.click()

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, coins_page))
        )
        name_elements = driver.find_elements(By.XPATH, '//div/a/b')
        symbol_elements = driver.find_elements(By.XPATH, '//div/small')
        logger.info(name_elements)
        new_coins = {}
        for name, symbol in zip(name_elements, symbol_elements):
            new_coins[name.text] = AllCoins(
                id=name.text,
                symbol=symbol.text,
                name=name.text,
                is_shit=False
            )
    logger.info(
        f"{'-'*30}\nGot {len(new_coins.keys())} coind from miningpoolstatszn")
    update_all_coins(new_coins)


if __name__ == "__main__":
    mining_pool_stats()
