from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import logging

from backend.utils.scrappers import scrap_website_driver


logger = logging.getLogger("__name__")

DEBUG = True


def btc_talk():
    today_lines = []
    with scrap_website_driver("https://bitcointalk.org/") as driver:
        coins_page = "//a[text()='Announcements (Altcoins)']"
        alts = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, coins_page))
        )
        time.sleep(3)
        alts.click()
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        trs = soup.find_all("tr")
        for tr in trs:
            if "Today" in tr.text:
                line = [td.text.strip() for td in tr.find_all("td")][2]
                if "[ANN] " in line and "»" not in line:
                    today_lines.append(line.split("[ANN] ")[1].strip())

    return today_lines


if __name__ == "__main__":
    todays = btc_talk()
    with open("btc_text", "a") as f:
        for line in todays:
            f.write(line + "\n")
