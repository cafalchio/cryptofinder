from backend.scrappers.run_scrappers import update_all_coins
from backend.utils.utils import fetch_data
from backend.data.models import AllCoins


def coingecko():
    new_coins = []
    url = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"
    response = fetch_data(url)
    data = response.json()
    new_coins = {}
    for coin in data:
        new_coins[coin["id"]] = AllCoins(id=coin['id'], symbol=coin['symbol'],
                                         name=coin['name'], is_shit=False)

    update_all_coins(new_coins)
