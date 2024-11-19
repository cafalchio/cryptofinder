from app.app import create_app, ConfigApp
import sys
from backend import scrappers


CONFIG_FILE = "environments.json"


def config_app(env):
    config = ConfigApp(environment=env, config_file=CONFIG_FILE)
    flask_app = create_app(config)
    return flask_app, config


if __name__ == "__main__":
    if "prod" in sys.argv:
        flask_app, config = config_app("DEV")
    else:
        flask_app, config = config_app("DEV")

    if "scrappers" in sys.argv or "scrapper" in sys.argv:
        print(f"\n---------- Running Scrapper ----------\n")
        for scrapper_name in config.scrappers.keys():
            scrapper_class = getattr(scrappers, scrapper_name)
            if config.scrappers[scrapper_name]["enabled"]:
                print(f"Running: {scrapper_class.__name__}")
                scrapper = scrapper_class(config)
                scrapper.run()

    print(f"{config.HOST}:{config.PORT} - DEBUG: {config.DEBUG}")
    flask_app.run(host=config.HOST, debug=config.DEBUG, port=config.PORT)
