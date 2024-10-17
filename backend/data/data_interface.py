import os
import logging
import pandas as pd
from pandas.errors import EmptyDataError

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
