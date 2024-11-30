from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from app.app import get_logger
from backend.data.models import AllCoins
from backend.utils.scrappers import BaseScrapper, ScrapperError, scrap_website_driver
import re

logger = get_logger()

EXCLUDE = ["POW", "POS", "BETA", "PRE", "ANN", "ICO", "All"]


class BtcTalk(BaseScrapper):
    def run(self):
        scrap_config = self.config.scrappers[self.name]
        if not scrap_config["enabled"]:
            return

        today_lines = []
        with scrap_website_driver(scrap_config["url"]) as driver:
            alts = WebDriverWait(driver, scrap_config["timeout"]).until(
                EC.element_to_be_clickable(
                    (By.XPATH, scrap_config["XPATHS"][0]))
            )
            alts.click()
            soup = BeautifulSoup(driver.page_source, "html.parser")
            trs = soup.find_all("tr")
            new_coins = {}
            for tr in trs:
                if "Today" in tr.text:
                    line = [td.text.strip() for td in tr.find_all("td")][2]
                    with open("btc_talk_data", "a") as f:
                        f.write(line)
                    if "ANN" not in line or "Topics" in line:
                        continue
                    line = clean_text(line)
                    name, symbol = extract(line)
                    name = name.replace(symbol, "")
                    try:
                        name = " ".join(name.split(" ")[0:3])
                    except ScrapperError:
                        name = line
                    new_coins[name] = AllCoins(
                        id=name.lower(),
                        symbol=symbol,
                        name=name,
                        source="btc talk",
                        is_shit=False,
                    )
            self.update_all_coins(new_coins)
        return today_lines


def clean_text(text):
    for word in EXCLUDE:
        text = text.replace(word, " ")
    text = re.sub(r'[^\x00-\x7F]', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.replace("  ", " ").strip().lstrip()
    return text


def extract(line):
    name = ""
    symbol = ""
    symbol_re = r'\b[A-Z]{3,5}\b'
    group = re.findall(symbol_re, line)
    symbol = next((g for g in group if g not in EXCLUDE), "")
    name = line.replace(symbol, "")
    name = name.strip()
    symbol = symbol.strip()
    return name, symbol
