from backend.scrappers.run_scrappers import update_new_coins
from backend.utils.utils import fetch_data
from backend.data.models import NewCoins


def coingecko():
    new_coins = []
    url = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"
    response = fetch_data(url)
    data = response.json()
    new_coins = [NewCoins(id=coin['id'], symbol=coin['symbol'],
                          name=coin['name'], is_shit=False) for coin in data]

    update_new_coins(new_coins)
