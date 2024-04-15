import time
from datetime import datetime

import pandas as pd
from data import fetch_data, get_nested_data
import logging

logger = logging.getLogger(__name__)


class Coingecko:
    new_coins = None
    BASE_URL = "https://api.coingecko.com/api/v3/coins/list"
    ALL_COINS = "static/all_coins.csv"

    def run_sequence(self):
        logger.info("Running get all new coins")
        self.get_new_coins()
        self.get_details()

    @property
    def fetch_coins(self):
        return fetch_data(self.BASE_URL)

    @property
    def all_saved_coins(self):
        try:
            return pd.read_csv(self.ALL_COINS)
        except FileNotFoundError:
            return pd.DataFrame({"id": []})

    def get_new_coins(self):
        difference = set(self.all_saved_coins['id']) - set(self.fetch_coins['id'])
        new_coins = self.fetch_coins[self.fetch_coins['id'].isin(difference)]
        all_coins = pd.concat([self.all_saved_coins, self.fetch_coins], ignore_index=True)
        all_coins.to_csv(self.ALL_COINS, index=False)
        return new_coins

    def get_details(self):
        coins = []
        urls = [
            f"https://api.coingecko.com/api/v3/coins/{id}?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false"
            for id in self.new_coins["id"]]
        for url in urls:
            response = fetch_data(url)
            time.sleep(10)
            coins.append(self.parse_coin_details(response))
        return coins

    def parse_coin_details(self, details):
        data_to_load = {
            "id": get_nested_data(details, "id"),
            "symbol": get_nested_data(details, "symbol"),
            "name": get_nested_data(details, "name"),
            "contract_address": get_nested_data(details, "contract_address"),
            "categories": get_nested_data(details, "categories"),
            "hashing_algorithm": get_nested_data(details, "hashing_algorithm"),
            "asset_platform_id": get_nested_data(details, "asset_platform_id"),
            "date": datetime.now().strftime("%Y/%m/%d")
        }
        return data_to_load

if __name__ == "__main__":
    coingecko = Coingecko()
    print(coingecko.get_new_coins())
