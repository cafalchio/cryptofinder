from app.config_app import get_logger

logger = get_logger()


def run_scrappers(config):
    # Avoid circular import
    from btc_talk import btc_talk
    from coingecko import coingecko
    from backend.scrappers.exchanges import xeggex
    from pools import rplant_xyz, miningpoolstats

    # For now, add the list of functions here
    logger.info("Running Scrappers ..")
    rplant_xyz.rplant(config)
    coingecko.coingecko(config)
    miningpoolstats.mining_pool_stats(config)
    xeggex.xeggex(config)
    btc_talk.btc_talk(config)
