from app.app import create_app, ConfigApp
import sys
from backend import scrappers


CONFIG_FILE = "environments.json"


def config_app(env):
    config = ConfigApp(environment=env, config_file=CONFIG_FILE)
    flask_app = create_app(config)
    return flask_app, config


def run_scrappers(config):
    print("\n---------- Running Scrapper ----------\n")
    for scrapper_name in config.scrappers.keys():
        scrapper_class = getattr(scrappers, scrapper_name)
        if config.scrappers[scrapper_name]["enabled"]:
            print(f"Running: {scrapper_class.__name__}")
            scrapper = scrapper_class(config)
            scrapper.run()


if __name__ == "__main__":
    env = "DEV" if "dev" in sys.argv else "PROD"
    scrap = "scrappers" in sys.argv or "scrapper" in sys.argv
    if env == "PROD":
        flask_app, config = config_app("PROD")
    else:
        flask_app, config = config_app("DEV")
        print(f"{config.HOST}:{config.PORT} - DEBUG: {config.DEBUG}")
    if scrap:
        run_scrappers(config)

    print(f"Running {env}")
    flask_app.run(host=config.HOST, debug=config.DEBUG, port=config.PORT)
