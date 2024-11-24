

from backend.data.models import AllCoins
from backend.utils.scrappers import BaseScrapper, scrap_website_soup
import logging


logger = logging.getLogger(__name__)


class Coinranking(BaseScrapper):
    def run(self):
        scrap_config = self.config.scrappers[self.name]
        if not scrap_config["enabled"]:
            return
        new_coins = {}

        for url in scrap_config["url"]:
            with scrap_website_soup(url) as soup:
                profiles = soup.find_all('span', class_='profile__name')
                for profile in profiles:
                    try:
                        name = profile.find(
                            'a', class_='profile__link').text.strip()
                        symbol = profile.find(
                            'span', class_='profile__subtitle-name').text.strip()
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
