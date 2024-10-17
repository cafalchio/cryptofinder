import os
import logging
import pandas as pd
from pandas.errors import EmptyDataError
from app.config_app import NEW_COINS, ALL_COINS, NEW_COINS_DETAILS

logger = logging.getLogger(__name__)
dir_path = os.path.dirname(os.path.abspath(__file__))
DATAFILES = "data"


class Interface:
    @staticmethod
    def read_data(data_file):
        print(pd.read_csv(data_file).to_json(orient="records"))
        try:
            return pd.read_csv(data_file).to_json(orient="records")
        except FileNotFoundError:
            logger.error(f"Could not find {data_file}")
            return []
        except EmptyDataError:
            logger.error(f"No data found in {data_file}")
            return []

    @property
    def all_coins(self):
        return self.read_data(os.path.join(dir_path, DATAFILES, "all_coins.csv"))

    @property
    def new_coins(self):
        return self.read_data(os.path.join(dir_path, DATAFILES, "new_coins.csv"))

    @property
    def new_coins_details(self):
        return self.read_data(os.path.join(dir_path, DATAFILES, "new_coins_details.csv"))


class DataInterface:
    def get_new_coins(self):
        new_coins_df = pd.read_csv(NEW_COINS)
        if len(new_coins_df) > 0:
            message = "New coins found!"
        else:
            message = "No new coins found"
        new_coins = new_coins_df.to_dict(
            "records") if not new_coins_df.empty else []
        return message, new_coins

    def get_all_coins(self):
        all_coins_df = pd.read_csv(ALL_COINS)
        all_coins = all_coins_df.to_dict(
            "records") if not all_coins_df.empty else []
        return all_coins

    def get_latest_coins(self):
        latest_coins_df = pd.read_csv(NEW_COINS_DETAILS)
        coins = latest_coins_df.to_dict(
            "records") if not latest_coins_df.empty else []
        return coins

    def shitcoins_by_contract(self):
        latest_coins_df = pd.read_csv(NEW_COINS_DETAILS)
        return self.filter_shitcoins_by_contract(latest_coins_df)

    def filter_shitcoins_by_contract(self, coins_df):
        """
        Mark as shitcoins all the tokens from other networks
        """
        filtered_coins = coins_df[coins_df['contract_address'] != ""]
        if len(filtered_coins) > 1:
            filtered_coins = filtered_coins.to_dict()
        return filtered_coins
