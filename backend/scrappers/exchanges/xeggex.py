from backend.data.models import AllCoins
from backend.utils.scrappers import BaseScrapper, scrap_website_soup
import logging
import re


logger = logging.getLogger(__name__)


class Xeggex(BaseScrapper):
    def run(self):
        scrap_config = self.config.scrappers["xeggex"]

        new_coins = {}
        pattern = re.compile(r"Announcing the New Listing of (.*) \((.*)\)")

        with scrap_website_soup(scrap_config["url"]) as soup:
            matches = re.findall(pattern, soup.text)
            if not matches:
                return
            for match in matches:
                name, symbol = match
                new_coins[name] = AllCoins(
                    id=name, symbol=symbol, name=name, source="xeggex", is_shit=False
                )
        self.update_all_coins(new_coins)
