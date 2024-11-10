from app.config_app import get_logger
from backend.scrappers.pools.rplant_xyz import Rplant

logger = get_logger()


def run_scrappers(config):
        
    _scrappers = {
        "rplant": Rplant,
    }
    for scrapper_config in config.scrappers:
        scrapper = _scrappers[scrapper_config.name]
        scrapper(scrapper_config).run()
   