from app.app import create_app, ConfigApp
import sys
from backend import scrappers


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
        for scrapper_name in config.scrappers.keys():
            scrapper_class = getattr(scrappers, scrapper_name)
            print(f"Running: {scrapper_class.__name__}")
            scrapper = scrapper_class(config)
            scrapper.run()

    print(f"\n---------- Starting {env} Server----------\n")
    print(f"{config.HOST}:{config.PORT} - DEBUG: {config.DEBUG}")
    flask_app.run(host=config.HOST, debug=config.DEBUG, port=config.PORT)
