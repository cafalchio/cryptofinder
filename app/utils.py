import pandas as pd
import logging

logger = logging.getLogger(__name__)

class Table:
    TODAY = "data/today.csv"
    YESTERDAY = "data/yesterday.csv"

    def get_differences(self):
        today = self.get_today()
        yesterday = self.get_yesterday()
        diff_index = [id for id in today.coin_id if id not in iter(yesterday.coin_id)]
        return diff_index


    def get_today(self):
        df = pd.read_csv(self.TODAY)
        return df

    def get_yesterday(self):
        df = pd.read_csv(self.YESTERDAY)
        return df
