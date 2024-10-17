import time
from datetime import datetime
import requests
import pandas as pd
from fastapi import requests

from utils import fetch_data, get_nested_data
import logging

logger = logging.getLogger(__name__)


class Coingecko:
    new_coins = None


    def run(self):
        logger.info("------ Running Coingecko -------")
        self.get_coins()
        # self.get_details()

    @staticmethod
    def fetch_coins(url):
        return fetch_data(url)

    def get_coins(self):
        url = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"
        df = fetch_data(url)
        return df[df.platforms == {}].drop("platforms", axis=1)

    def get_details(self, coins):
        urls = [
            f"https://api.coingecko.com/api/v3/coins/{id}?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false"
            for id in self.new_coins["id"]
        ]
        for url in urls:
            response = fetch_data(url)
            coins.append(self.parse_coin_details(response))
        coins = pd.DataFrame(coins)
        coins.sort_values(by="id").to_csv(NEW_COINS_DETAILS, index=False)
        return coins

    def parse_new_coins(self, data):
        data_to_load = {
            "id": get_nested_data(data, "id"),
            "symbol": get_nested_data(data, "symbol"),
            "name": get_nested_data(data, "name"),
            "platforms": get_nested_data(data, "platforms"),
        }
        if data.platforms != {}:
            return None
        return data_to_load

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
    # coingecko.run_sequence()
