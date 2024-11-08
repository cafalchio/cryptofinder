from app.config_app import get_logger

logger = get_logger()


def run_scrappers():
    # Avoid circular import
    from btc_talk import btc_talk
    from coingecko import coingecko
    from backend.scrappers.exchanges import xeggex
    from pools import rplant_xyz, miningpoolstats

    # For now, add the list of functions here
    logger.info("Running Scrappers ..")
    rplant_xyz.rplant()
    coingecko.coingecko()
    miningpoolstats.mining_pool_stats()
    xeggex.xeggex()
    btc_talk.btc_talk()




if __name__ == "__main__":
    run_scrappers()
