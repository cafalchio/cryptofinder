import json
import logging
import time

import pandas as pd
import requests
from requests import HTTPError


def convert_df_dict(df):
    if not df.empty:
        return df.to_dict('records')
    return {}


def get_data(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return json.dumps(response.json())


class Coingecko:
    coins = None
    BASE_URL = "https://api.coingecko.com/api/v3/coins/list"
    ALL_COINS = ""

    @property
    def coins(self):
        pass

    def get_new_coins(self, fetched_coins_df):
        new_coins = self.coins[~fetched_coins_df["id"].isin(self.coins["id"])]
        self.coins = pd.concat([self.coins, fetched_coins_df], ignore_index=True)
        self.coins.to_csv(self.ALL_COINS, index=False)
        return new_coins

    def parse_coins(self):
        pass

    def parse_details(self):
        pass
