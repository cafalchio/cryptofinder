import logging
import os
import requests
import pandas as pd
from datetime import datetime
import time

logging.basicConfig(
    # filename="app.log",
    # filemode="a",
    format="%(asctime)s-%(name)s-%(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)

logging.info("Running Utils.py")
logger = logging.getLogger("cryptofinder")


dir_path = os.path.dirname(os.path.abspath(__file__))
ALL_COINS = os.path.join(dir_path, "all_coins.csv")
NEW_COINS = os.path.join(dir_path, "new_coins.csv")
NEW_COINS_DETAILS = os.path.join(dir_path, "new_coins_details.csv")


def run_compare_coins():
    all_coins_df = pd.read_csv(ALL_COINS)
    new_coins_df = fetch_new_coins()
    new_coins_df = new_coins_df[~new_coins_df["id"].isin(all_coins_df["id"])]
    if len(new_coins_df) < 0:
        return new_coins_df, "No new coins!"
    save_all_coins(new_coins_df, all_coins_df)
    fetch_coins_details(new_coins_df.id.to_list())
    return new_coins_df, f"{len(new_coins_df)} new coins found"


def save_all_coins(new_coins_df, all_coins_df):
    all_coins_df = pd.concat([all_coins_df, new_coins_df], ignore_index=True)
    all_coins_df.to_csv(ALL_COINS, index=False)
    new_coins_df.to_csv(NEW_COINS, index=False)


def fetch_new_coins():
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url, timeout=5)
    logger.info(f"Fetch data: from {url} : {response.status_code}")
    if response.status_code == 200:
        coins_data = response.json()
        coins_df = pd.DataFrame(coins_data)
        now = datetime.now().strftime("%Y/%m/%d")
        coins_df["added"] = now
    else:
        logger.error(
            f"Failed to get data from Coingecko: {response.status_code}")
        return pd.DataFrame([])
    return coins_df


def select_json_data(json_data):
    # Extract data from JSON response

    data_to_load = {
        "Id": json_data.get("id"),
        "Symbol": json_data.get("symbol"),
        "Name": json_data.get("name"),
        # Taking the first category if available
        "Categories": json_data.get("categories", []),
        "Description": json_data.get("description", {}).get("en"),
        "Homepage": json_data.get("links", {}).get("homepage", [None]),
        "White paper": json_data.get("links", {}).get("whitepaper"),
        "Blockchain site": json_data.get("links", {}).get("blockchain_site", [None]),
        "contract_address": json_data.get("detail_platforms", {}).get("contract_address", "")
    }

    data_to_load["added"] = datetime.now().strftime("%Y/%m/%d")
    return pd.DataFrame([data_to_load])


def fetch_coins_details(ids):
    logger.info(f"Getting details for {ids}")
    new_coins_details_df = pd.DataFrame()
    for id in ids:
        url = (
            "https://api.coingecko.com/api/v3/coins/"
            + id
            + "?localization=false&tickers=false&market_data=false"
        )
        logger.info(f"Fetching details of {id}")
        response = requests.get(url, timeout=5)
        logger.info(f"Fetch data: from {id} : {response.status_code}")
        if response.status_code == 200:
            coin_data = response.json()
            new_coins_details_df = pd.concat(
                [new_coins_details_df, select_json_data(coin_data)], ignore_index=True
            )
        else:
            logger.error(
                f"Failed to fetch data from {url}: Status code {response.status_code}"
            )
        time.sleep(8)
    new_coins_details_df.to_csv(NEW_COINS_DETAILS, index=False)


if __name__ == "__main__":
    # print(fetch_coins_details(["dogita"]))
    print(run_compare_coins())
