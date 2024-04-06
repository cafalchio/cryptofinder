import requests
import pandas as pd
import os
import glob
from datetime import datetime

coin_logs_folder = 'coin_logs'
new_coins_folder = 'new_coins_found'


def get_latest_file(folder):
    files = glob.glob(f'{folder}/*.csv')
    if not files:
        return None
    return max(files, key=os.path.getctime)


def get_next_filename(folder, suffix):
    now = datetime.now()
    date_str = now.strftime('%Y%m%d')
    time_str = now.strftime('t%H%M%S')
    files = glob.glob(f'{folder}/{date_str}{suffix}*.csv')
    if not files:
        return f"{date_str}_{time_str}{suffix}.csv"
    return f"{date_str}_{time_str}{suffix}.csv"


def store_csv(df, folder, filename):
    os.makedirs(folder, exist_ok=True)
    file_path = f"{folder}/{filename}"
    df.to_csv(file_path, index=False)
    return file_path


def fetch_and_compare_coins():
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    coins_data = response.json() if response.status_code == 200 else []

    coins_df = pd.DataFrame(coins_data)

    new_fetch_filename = get_next_filename(coin_logs_folder, "-log")

    latest_file_path = get_latest_file(coin_logs_folder)
    new_coins_df = pd.DataFrame()

    if latest_file_path:
        latest_coins_df = pd.read_csv(latest_file_path)
        new_coins_df = coins_df[~coins_df['id'].isin(latest_coins_df['id'])]

    if not new_coins_df.empty:
        new_coins_count = len(new_coins_df)
        new_coins_filename = get_next_filename(
            new_coins_folder, suffix=f"-{str(new_coins_count).zfill(2)}_new_found")
        store_csv(new_coins_df, new_coins_folder, new_coins_filename)
        message = ""
    else:
        message = "No new coins found."

    store_csv(coins_df, coin_logs_folder, new_fetch_filename)

    coins = new_coins_df.to_dict('records') if not new_coins_df.empty else []

    return coins, message
