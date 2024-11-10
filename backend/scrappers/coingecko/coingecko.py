from app.config_app import get_logger
from backend.data.models import AllCoins
from backend.utils.scrappers import BaseScrapper

logger = get_logger()


class Coinbase(BaseScrapper):
    def run(self):
        breakpoint()
        scrap_config = self.config.scrappers["coinbase"]
        response = self.fetch_data(scrap_config)
        data = response.json()
        new_coins = {}
        for coin in data:
            new_coins[coin["id"]] = AllCoins(
                id=coin["id"],
                symbol=coin["symbol"],
                name=coin["name"],
                source="coinbase",
                is_shit=False,
            )
        self.update_all_coins(new_coins)
