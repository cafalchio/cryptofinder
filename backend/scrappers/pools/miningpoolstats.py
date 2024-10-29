from tools import scrap_website_soup, scrap_website_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

logger = logging.getLogger("__name__")
DEBUG = True

with scrap_website_driver("https://miningpoolstats.stream/newcoins") as driver:

    consent_button = "//button[@aria-label='Consent']"
    coins_page = "//*[@id='mainpage']"

    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, consent_button))
    )
    logger.info(button)
    if DEBUG:
        time.sleep(10)

    button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, coins_page))
    )

    if DEBUG:
        time.sleep(10)

    elements = driver.find_elements(By.CLASS_NAME, "fc-button-label")

    for element in elements:
        coin_name = element.text
        coin_link = element.get_attribute("href")
        print(f"Coin: {coin_name}, Link: {coin_link}")
