from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging

from backend.scrappers.pools.tools import scrap_website_driver

logger = logging.getLogger(__name__)


def rplant():
    with scrap_website_driver("https://pool.rplant.xyz/") as driver:
        coins_page = "//*[@id='tbs-table']"

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, coins_page))
        )
        name_elements = driver.find_elements(By.XPATH, '//tbody/tr/td')
        name_elements = [
            td for td in name_elements if 'sorting_1' in td.get_attribute('class')]
        logger.info(name_elements)

        for name in name_elements:
            logger.info(f"name: {name.text}")


if __name__ == "__main__":
    rplant()
