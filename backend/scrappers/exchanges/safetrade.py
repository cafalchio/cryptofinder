from backend.data.models import AllCoins
from bs4 import BeautifulSoup
from backend.utils.scrappers import BaseScrapper, scrap_website_driver, scrap_website_soup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class SafeTrade(BaseScrapper):
    def run(self):
        scrap_config = self.config.scrappers[self.name]
        if not scrap_config["enabled"]:
            return
        new_coins = {}
        for url in scrap_config["url"]:
            with scrap_website_driver(url) as driver:
                WebDriverWait(driver, scrap_config["timeout"]).until(
                    lambda d: d.execute_script(
                        "return document.readyState") == "complete"
                )
                soup = BeautifulSoup(driver.page_source, "html.parser")
                elements = soup.find_all("div", class_="z-table-row")
                for element in elements:
                    try:
                        name = element.find("span", class_="name").text.strip()
                        symbol = element.find(
                            "span", class_="code").text.strip()

                    except TypeError:
                        continue
                    new_coins[name] = AllCoins(
                        id=name.lower(),
                        symbol=symbol,
                        name=name,
                        source=self.name,
                        is_shit=False,
                    )
        self.update_all_coins(new_coins)
