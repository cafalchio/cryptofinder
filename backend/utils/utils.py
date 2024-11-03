import time
import requests
import logging
from app.config_app import COINGECKO_API

logger = logging.getLogger(__name__)


def fetch_data(url):
    headers = {"accept": "application/json", "x-cg-demo-api-key": COINGECKO_API}
    tries = 3
    for i in range(0, tries):
        logger.info(f"Getting data for {url}")
        time.sleep(10)
        response = requests.get(url=url, headers=headers, timeout=10)
        logger.info(f"Response: {response.status_code}")
        response.raise_for_status()
        return response


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
