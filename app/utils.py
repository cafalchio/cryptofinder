import logging
import requests
import pandas as pd


logger = logging.getLogger('scheduler')

ALL_COINS = "coin_logs/all_coins.csv"
NEW_COINS = "coin_logs/new_coins.csv"


def run_compare_coins():
    all_coins_df = pd.read_csv(ALL_COINS)
    new_coins_df = fetch_new_coins()
    new_coins_df = new_coins_df[~new_coins_df['id'].isin(all_coins_df['id'])]
    if len(new_coins_df) < 0:
        return new_coins_df, "No new coins!"
    save_all_coins(new_coins_df, all_coins_df)
    return new_coins_df, f"{len(new_coins_df)} new coins found"


def save_all_coins(new_coins_df, all_coins_df):
    all_coins_df = pd.concat([all_coins_df, new_coins_df], ignore_index=True)
    all_coins_df.to_csv(ALL_COINS, index=False)
    new_coins_df.to_csv(NEW_COINS, index=False)


def fetch_new_coins():
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    logger.info(f"Fetch data: from {url} : {response.status_code}")
    if response.status_code == 200:
        coins_data = response.json()
    else:
        logger.error(
            f"Failed to get data from Coingecko: {response.status_code}")
        return pd.DataFrame([])
    return pd.DataFrame(coins_data)


if __name__ == "__main__":
    run_compare_coins()
