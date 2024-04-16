import time
from datetime import datetime
from functools import cache

import pandas as pd
from data import fetch_data, get_nested_data
import logging

logger = logging.getLogger(__name__)


class Coingecko:
    new_coins = None
    BASE_URL = "https://api.coingecko.com/api/v3/coins/list"
    ALL_COINS = "datafiles/all_coins.csv"
    NEW_COINS = "datafiles/new_coins.csv"
    NEW_COINS_DETAILS = "datafiles/new_coins_details.csv"

    def run(self):
        logger.info("------ Running Coingecko -------")
        self.get_new_coins()
        self.get_details()

    @property
    @cache
    def fetch_coins(self):
        return fetch_data(self.BASE_URL)

    @property
    def all_saved_coins(self):
        try:
            return pd.read_csv(self.ALL_COINS)
        except FileNotFoundError:
            return pd.DataFrame({"id": []})

    def get_new_coins(self):
        new_coins = self.fetch_coins[~self.fetch_coins['id'].isin(self.all_saved_coins['id'])]
        new_coins.drop_duplicates(subset=['id']).to_csv(self.NEW_COINS, index=False)
        all_coins = pd.concat([self.all_saved_coins, self.fetch_coins], ignore_index=True)
        all_coins.drop_duplicates(subset=['id']).sort_values(by="id").to_csv(self.ALL_COINS, index=False)

    def get_details(self):
        if len(self.new_coins) == 0:
            return []
        coins = []
        urls = [
            f"https://api.coingecko.com/api/v3/coins/{id}?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false"
            for id in self.new_coins["id"]]
        for url in urls:
            response = fetch_data(url)
            time.sleep(10)
            coins.append(self.parse_coin_details(response))
        coins = pd.DataFrame(coins)
        coins.sort_values(by="id").to_csv(self.NEW_COINS_DETAILS, index=False)
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
    coingecko.run_sequence()
