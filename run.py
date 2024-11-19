from app.app import create_app, ConfigApp
import sys
from backend.scrappers import scrapper_runner


config = ConfigApp(environment="PROD", config_file="environments.json")

flask_app = create_app(config)


if __name__ == "__main__":
    if "prod" in sys.argv:
        config = ConfigApp("PROD")
        env = "Production"
    else:
        config = ConfigApp("DEV")
        env = "Development"

    if "scrappers" in sys.argv or "scrapper" in sys.argv:
        print(f"\n---------- Running Scrapper {env} ----------\n")
        scrapper_runner.run_scrappers(config)

    print(f"\n---------- Starting {env} Server----------\n")
    flask_app.run(host=config.HOST, debug=config.DEBUG, port=config.PORT)
