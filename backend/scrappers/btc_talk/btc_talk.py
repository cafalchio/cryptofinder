from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

from app.config_app import get_logger
from backend.data.models import AllCoins
from backend.utils.scrappers import scrap_website_driver
from backend.utils.utils import update_all_coins

logger = get_logger()


def extract_name(line):
    line = line[6:]
    symbol = ""
    if ":" in line:
        name = line.split(":")[0]
    elif "-" in line:
        name = line.split("-")[0]
    else:
        name = line.split(" ")[0]
        symbol = line.split(" ")[1]
    return name, symbol


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
        new_coins = {}
        for tr in trs:
            if "Today" in tr.text:
                line = [td.text.strip() for td in tr.find_all("td")][2]
                if "[ANN] " in line and "»" not in line:
                    name, symbol = extract_name(line)
                    new_coins[name] = AllCoins(
                        id=name,
                        symbol=symbol,
                        name=name,
                        source="btc talk",
                        is_shit=False,
                    )
                    line = line.split("[ANN] ")[1].strip()
                    today_lines.append(line)
                    logger.info(line)
        logger.info(f"-Got {len(new_coins.keys())} coins from rplantxyz")
        update_all_coins(new_coins)
    return today_lines


if __name__ == "__main__":
    todays = btc_talk()
    with open("btc_text", "a") as f:
        for line in todays:
            print(line)
            f.write(line + "\n")
