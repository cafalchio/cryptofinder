from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from app.config_app import get_logger
from backend.data.models import AllCoins
from backend.utils.scrappers import BaseScrapper, scrap_website_driver

logger = get_logger()


class BtcTalk(BaseScrapper):
    def run(self):
        scrap_config = self.config.scrappers["btc_talk"]

        today_lines = []

        with scrap_website_driver(scrap_config["url"]) as driver:
            alts = WebDriverWait(driver, scrap_config["timeout"]).until(
                EC.element_to_be_clickable((By.XPATH, scrap_config["XPATHS"][0]))
            )
            alts.click()
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            trs = soup.find_all("tr")
            new_coins = {}
            for tr in trs:
                if "Today" in tr.text:
                    line = [td.text.strip() for td in tr.find_all("td")][2]
                    if "[ANN] " in line and "»" not in line:
                        name, symbol = self.extract_name(line)
                        new_coins[name] = AllCoins(
                            id=name,
                            symbol=symbol,
                            name=name,
                            source="btc talk",
                            is_shit=False,
                        )
                        line = line.split("[ANN] ")[1].strip()
                        print(line)
                        today_lines.append(line)
                        logger.info(line)
            self.update_all_coins(new_coins)
        return today_lines

    def extract_name(self, line):
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
