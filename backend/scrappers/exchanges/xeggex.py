from backend.data.models import NewCoins
from backend.scrappers.run_scrappers import update_new_coins
from backend.utils.scrappers import scrap_website_soup
import logging
import re

logger = logging.getLogger(__name__)


def xeggex():
    new_coins = {}
    pattern = re.compile(r"Announcing the New Listing of (.*) \((.*)\)")

    with scrap_website_soup("https://xeggex.com/news") as soup:
        matches = re.findall(pattern, soup.text)
        if not matches:
            return
        for match in matches:
            name, symbol = match
            new_coins[name] = NewCoins(
                id=name,
                symbol=symbol,
                name=name,
                is_shit=False
            )
    logger.info(f"{'-'*30}\nGot {len(new_coins.keys())} coind from rplantxyz")
    update_new_coins(new_coins)


if __name__ == "__main__":
    xeggex()
