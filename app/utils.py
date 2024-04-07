import os
import requests
import pandas as pd
from datetime import datetime
from app.run import logger

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
        "Categories": json_data.get("categories", [None])[
            0
        ],  # Taking the first category if available
        "Description": json_data.get("description", {}).get("en"),
        "Homepage": json_data.get("links", {}).get("homepage", [None])[
            0
        ],  # Taking the first homepage link if available
        "White paper": json_data.get("links", {}).get("whitepaper"),
        "Blockchain site": json_data.get("links", {}).get("blockchain_site", [None])[
            0
        ],  # Taking the first blockchain site if available
        "Large": json_data.get("image", {}).get("large"),
    }
    # Add the 'Added at' column with the current date and time
    data_to_load["added"] = datetime.now().strftime("%Y/%m/%d")
    # Create a DataFrame from the processed data
    return pd.DataFrame([data_to_load])


def fetch_new_coins_details():
    # Initialize an empty DataFrame to store all the data
    new_coins_details_df = pd.DataFrame()
    # Reading csv and making a list with values of the first column
    new_coins_df = pd.read_csv(NEW_COINS)
    new_coins = new_coins_df["id"].tolist()
    # fetch details of each new coin and stores in a dataframe
    for new_coin in new_coins:
        url = (
            "https://api.coingecko.com/api/v3/coins/"
            + new_coin
            + "?localization=false&tickers=false&market_data=false"
        )
        response = requests.get(url)
        logger.info(f"Fetch data: from {url} : {response.status_code}")
        if response.status_code == 200:
            coin_data = response.json()
            # Convert the JSON data to a DataFrame
            new_coins_details_df = pd.concat(
                [new_coins_details_df, select_json_data(coin_data)], ignore_index=True
            )
        else:
            logger.error(
                f"Failed to fetch data from {url}: Status code {response.status_code}"
            )
    new_coins_details_df.to_csv(NEW_COINS_DETAILS, index=False)


if __name__ == "__main__":

    print(run_compare_coins())
