import time

import pandas as pd
import requests


def convert_df_dict(df):
    if not df.empty:
        return df.to_dict('records')
    return {}


def fetch_data(url):
    tries = 3
    for i in range(0, tries):
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        if response.json():
            return pd.DataFrame(response.json())
        time.sleep(15)
    return pd.DataFrame([])


def get_nested_data(nested_dict, key):
    """I got help from gpt"""
    if isinstance(nested_dict, dict):
        if key in nested_dict:
            return nested_dict[key]
        for value in nested_dict.values():
            result = get_nested_data(value, key)
            if result is not None:
                return result
    elif isinstance(nested_dict, list):
        for item in nested_dict:
            result = get_nested_data(item, key)
            if result is not None:
                return result
    return None


if __name__ == "__main__":
    test_data = {
        "detail_platforms": {
        "": {
            "decimal_place": None,
            "contract_address": {"casa": [200]}}
        }
    }
    print(get_data(test_data, "casa"))
