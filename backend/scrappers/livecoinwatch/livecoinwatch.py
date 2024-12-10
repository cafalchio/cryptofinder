from app.app import get_logger
from backend.data.models import AllCoins
from backend.utils.scrappers import BaseScrapper

logger = get_logger()


class LiveCoinWatch(BaseScrapper):
    def run(self):
        scrap_config = self.config.scrappers[self.name]
        if not scrap_config["enabled"]:
            return
        response = self.fetch_data(scrap_config)
        data = response.json()
        new_coins = {}
        for coin in data:
            new_coins[coin["name"]] = AllCoins(
                id=coin["name"].lower(),
                symbol=coin["code"],
                name=coin["name"],
                source=self.name,
                is_shit=False,
            )
        self.update_all_coins(new_coins)