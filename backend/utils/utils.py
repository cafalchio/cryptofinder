import time
import requests
import logging
from app.app import create_app, db
from app.config_app import COINGECKO_API
from backend.data.models import AllCoins, NewCoins

logger = logging.getLogger(__name__)


class SaveDataError(Exception):
    logger.error("Could not save data to DB")
    pass


def save_coins_if_new(new_coins):

    app = create_app()
    with app.app_context():
        

        all_coins = db.session.execute(db.select(AllCoins)).scalars()
        old_coins = [coin["name"] for coin in all_coins]
        new_coins = [NewCoins(id=coin['id'], symbol=coin['symbol'],
                              name=coin['name'], is_shit=False) for coin in new_coins if coin["name"] not in old_coins]

        db.session.add_all(new_coins)
        try:
            db.session.commit()
        except SaveDataError:
            db.session.rollback()


def fetch_data(url):
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": COINGECKO_API
    }
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
