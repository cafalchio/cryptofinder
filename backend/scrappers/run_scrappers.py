from datetime import datetime, timedelta
from app.app import create_app, db
from backend.data.models import AllCoins
from sqlalchemy import select

from backend.scrappers.exchanges import xeggex


def run_scrappers():
    # Import scrapers
    from coingecko import coingecko
    from pools import rplant_xyz, miningpoolstats

    # For now, add the list of functions here
    # rplant_xyz.rplant()
    coingecko.coingecko()
    miningpoolstats.mining_pool_stats()
    xeggex.xeggex()
    rplant_xyz.rplant()


def update_all_coins(coins):
    if not coins:
        return
    app = create_app()
    with app.app_context():
        existing_all_coins = {coin.id for coin in db.session.execute(
            select(AllCoins)).scalars().all()}
        to_update = []

        for id, coin in coins.items():
            if id in existing_all_coins:
                continue
            to_update.append(AllCoins(
                id=coin.id,
                symbol=coin.symbol,
                name=coin.name,
                is_shit=False
            ))
        if to_update:
            db.session.bulk_save_objects(to_update)
            db.session.commit()


if __name__ == "__main__":
    run_scrappers()
