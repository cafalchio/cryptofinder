from datetime import datetime, timedelta
from app.app import create_app, db
from backend.data.models import AllCoins, NewCoins
from sqlalchemy import select, insert


def run_scrappers():
    # Import scrapers
    from coingecko import coingecko
    from pools import rplant_xyz, miningpoolstats

    expired_coins = get_expired_coins_by(hours=1)
    update_all_coins(expired_coins)

    # coingecko.coingecko()
    rplant_xyz.rplant()
    miningpoolstats.mining_pool_stats()


def get_expired_coins_by(hours=1):
    current_time = datetime.utcnow()
    expire_date = current_time - timedelta(hours=hours)

    app = create_app()
    with app.app_context():
        # Retrieve coins that have expired
        expired_coins = db.session.execute(
            select(NewCoins).where(NewCoins.added < expire_date)
        ).scalars().all()
    return expired_coins


def update_new_coins(coins):
    if not coins:
        return

    app = create_app()
    with app.app_context():
        existing_all_coins = {coin.id for coin in db.session.execute(
            select(AllCoins)).scalars().all()}
        existing_new_coins = {coin.id for coin in db.session.execute(
            select(NewCoins)).scalars().all()}
        to_update = []

        for id, coin in coins.items():
            if id in existing_all_coins or id in existing_new_coins:
                continue
            to_update.append(NewCoins(
                id=coin.id,
                symbol=coin.symbol,
                name=coin.name,
                is_shit=False
            ))
        if to_update:
            db.session.bulk_save_objects(to_update)
            db.session.commit()


def update_all_coins(coins):
    if not coins:
        return
    app = create_app()
    with app.app_context():
        existing_coins = {coin.id for coin in AllCoins.query.all()}
        to_update = []
        for coin in coins:
            if coin.id not in existing_coins:
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
