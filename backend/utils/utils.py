import time
import requests
import logging

from sqlalchemy import select
from app.app import create_app, db
from app.config_app import COINGECKO_API
from backend.data.models import AllCoins

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


def update_all_coins(coins):
    if not coins:
        return
    app = create_app()
    with app.app_context():
        existing_all_coins = {
            coin.id for coin in db.session.execute(select(AllCoins)).scalars().all()
        }
        to_update = []

        for id, coin in coins.items():
            if id in existing_all_coins:
                continue
            logger.info("Found coin: {id}")
            to_update.append(
                AllCoins(id=coin.id, symbol=coin.symbol, name=coin.name, is_shit=False)
            )
        if to_update:
            db.session.bulk_save_objects(to_update)
            db.session.commit()
