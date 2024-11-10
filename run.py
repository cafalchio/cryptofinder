from app.app import create_app, ConfigApp
import sys
from backend.scrappers import scrapper_runner


config = ConfigApp(environment="PROD", config_file="environments.json")

flask_app = create_app(config)


if __name__ == "__main__":
    if "prod" in sys.argv:
        config = ConfigApp("PROD")
    else:
        config = ConfigApp("DEV")

    env = "Development" if config.testing else "Production"
    print(f"\n---------- Starting {env} ----------\n")

    if "scrappers" in sys.argv:
        scrapper_runner.run_scrappers(config)
    flask_app.run(host=config.HOST, debug=config.DEBUG, port=config.PORT)
