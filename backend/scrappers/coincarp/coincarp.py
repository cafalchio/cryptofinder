from backend.data.models import AllCoins
from backend.utils.scrappers import BaseScrapper, scrap_website_soup
import logging


logger = logging.getLogger(__name__)


class CoinCarp(BaseScrapper):
    def run(self):
        scrap_config = self.config.scrappers[self.name]
        if not scrap_config["enabled"]:
            return
        new_coins = {}
        with scrap_website_soup(scrap_config["url"]) as soup:
            divs = soup.find_all("div", class_="name")
            for div in divs:
                try:
                    name = div.find("span", class_="fullname").text.strip()
                    symbol = div.find("span", class_="symbo").text.strip()
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
