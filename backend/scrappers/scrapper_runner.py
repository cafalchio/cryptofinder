from app.config_app import get_logger
from backend.scrappers.btc_talk.btc_talk import BtcTalk
from backend.scrappers.coingecko.coingecko import Coinbase
from backend.scrappers.exchanges.xeggex import Xeggex
from backend.scrappers.pools.miningpoolstats import MiningPoolStats
from backend.scrappers.pools.rplant_xyz import Rplant

logger = get_logger()


def run_scrappers(config):
    _scrappers = {
        "rplant": Rplant,
        "coinbase": Coinbase,
        "miningpoolstats": MiningPoolStats,
        "btc_talk": BtcTalk,
        "xeggex": Xeggex
    }
    for name, scrap_class in _scrappers.items():
        logger.info(f"Running scrapper {name}")
        scrapper = scrap_class(config)
        scrapper.run()
