from app.app import get_logger
from backend.data.models import AllCoins
from backend.utils.scrappers import BaseScrapper

logger = get_logger()


class Coingecko(BaseScrapper):
    def run(self):
        scrap_config = self.config.scrappers[self.name]
        if not scrap_config["enabled"]:
            return
        response = self.fetch_data(scrap_config)
        data = response.json()
        new_coins = {}
        for coin in data:
            new_coins[coin["id"]] = AllCoins(
                id=coin["id"],
                symbol=coin["symbol"],
                name=coin["name"],
                source=self.name,
                is_shit=False,
            )
        self.update_all_coins(new_coins)


# TODO: Filter coingecko coins based on details
