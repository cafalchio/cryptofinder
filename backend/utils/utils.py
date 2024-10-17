import time
import pandas as pd
import numpy as np
import requests
import logging

logger = logging.getLogger(__name__)


def convert_df_dict(df):
    if not df.empty:
        return df.to_dict('records')
    return {}


def fetch_data(url):
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": "CG-w4csxkgAMiBUnf4uy8DgpknE"
    }
    tries = 3
    for i in range(0, tries):
        logger.info(f"Getting data for {url}")
        time.sleep(10)
        response = requests.get(url=url, headers=headers, timeout=10)
        logger.info(f"Response: {response.status_code}")
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
    return None


