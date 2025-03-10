from app.app import create_app, ConfigApp, get_logger
import sys
from backend import scrappers
from concurrent.futures import ProcessPoolExecutor

CONFIG_FILE = "environments.json"

logger = get_logger()


def prRed(text, end=None):
    print(f"\033[31m {text}\033[00m", end=end)


def config_app(env):
    config = ConfigApp(environment=env, config_file=CONFIG_FILE)
    flask_app = create_app(config)
    return flask_app, config


def run_scrapper(scrapper_name):
    scrapper_class = getattr(scrappers, scrapper_name)
    if config.scrappers[scrapper_name]["enabled"]:
        print(f"Running: {scrapper_class.__name__} ", end="...")
        scrapper = scrapper_class(config)
        try:
            scrapper.run()
        except Exception as e:
            prRed(f"Fail {e}")
            logger.error(f"ERROR on: {scrapper_name} ")
            logger.error(f"Exception:\n{e}")
            return
    return


def run_scrappers(config):
    print("\n---------- Running Scrappers ----------\n")
    with ProcessPoolExecutor() as executor:
        executor.map(run_scrapper, config.scrappers.keys())


env = "DEV" if "dev" in sys.argv else "PROD"
scrap = "scrappers" in sys.argv or "scrapper" in sys.argv

if env == "PROD":
    flask_app, config = config_app("PROD")
else:
    flask_app, config = config_app("DEV")


if __name__ == "__main__":
    print(f"Running {env} config")
    run_scrappers(config)
