from app.config_app import get_logger
from backend.utils.utils import fetch_data, update_all_coins
from backend.data.models import AllCoins

logger = get_logger()


def coingecko():
    url = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"
    response = fetch_data(url)
    data = response.json()
    new_coins = {}
    for coin in data:
        new_coins[coin["id"]] = AllCoins(
            id=coin["id"], symbol=coin["symbol"], name=coin["name"], is_shit=False
        )

    update_all_coins(new_coins)
