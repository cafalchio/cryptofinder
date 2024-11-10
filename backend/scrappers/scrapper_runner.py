from app.config_app import get_logger
from backend.scrappers.coingecko.coingecko import Coinbase
from backend.scrappers.pools.rplant_xyz import Rplant

logger = get_logger()


def run_scrappers(config):
    _scrappers = {
        "rplant": Rplant,
        "coinbase": Coinbase,
    }
    for name, scrap_class in _scrappers.items():
        logger.info(f"Running scrapper {name}")
        scrapper = scrap_class(config)
        scrapper.run()
   