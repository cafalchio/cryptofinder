from backend.utils.scrappers import scrap_website_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

logger = logging.getLogger("__name__")


def mining_pool_stats():
    with scrap_website_driver("https://miningpoolstats.stream/newcoins") as driver:
        consent_button = "//button[@aria-label='Consent']"
        coins_page = "//*[@id='mainpage']"

        button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, consent_button))
        )
        logger.info(button)
        time.sleep(1)
        button.click()

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, coins_page))
        )
        name_elements = driver.find_elements(By.XPATH, '//div/a/b')
        symbol_elements = driver.find_elements(By.XPATH, '//div/small')
        logger.info(name_elements)

        for name, symbol in zip(name_elements, symbol_elements):
            print(f"{name.text} : {symbol.text}")


if __name__ == "__main__":
    mining_pool_stats()
