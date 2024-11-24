

from backend.data.models import AllCoins
from backend.utils.scrappers import BaseScrapper, scrap_website_soup
import logging


logger = logging.getLogger(__name__)


class Cryptoslate(BaseScrapper):
    def run(self):
        scrap_config = self.config.scrappers[self.name]
        if not scrap_config["enabled"]:
            return
        new_coins = {}

        for url in scrap_config["url"]:
            with scrap_website_soup(url) as soup:
                h3s = soup.find_all("h3")
                for h3 in h3s:
                    try:
                        name = h3.find("a", title=True)["title"]
                        symbol = h3.find('span', class_='ticker').text.strip()
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
