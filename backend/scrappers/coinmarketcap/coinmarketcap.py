from backend.data.models import AllCoins
from backend.utils.scrappers import BaseScrapper, scrap_website_soup
import logging


logger = logging.getLogger(__name__)


class CoinMarketCap(BaseScrapper):
    def run(self):
        scrap_config = self.config.scrappers[self.name]
        if not scrap_config["enabled"]:
            return
        new_coins = {}
        for url in scrap_config["url"]:
            with scrap_website_soup(url) as soup:
                rows = soup.find_all("tr", style="cursor:pointer")
                for row in rows:
                    tds = row.find_all("td")
                    if len(tds) >= 2 and tds[-2].text == "Own Blockchain":
                        for sp in row.find_all():
                            name_tag = sp.find(
                                "p", class_="sc-71024e3e-0 ehyBa-d")
                            symbol_tag = sp.find(
                                "p", class_="sc-71024e3e-0 OqPKt coin-item-symbol"
                            )
                            if name_tag and symbol_tag:
                                name = name_tag.text.strip()
                                symbol = symbol_tag.text.strip()
                                new_coins[name] = AllCoins(
                                    id=name.lower(),
                                    symbol=symbol,
                                    name=name,
                                    source=self.name,
                                    is_shit=False,
                                )
        self.update_all_coins(new_coins)
