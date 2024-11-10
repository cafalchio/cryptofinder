from app.app import create_app, ConfigApp
import sys
from backend.scrappers import scrapper_runner


if __name__ == "__main__":
    config = ConfigApp(environment="PROD", config_file="environments.json")

    if len(sys.argv) > 1:
        if sys.argv[2] == "prod":
            config = ConfigApp("PROD")

    env = "Development" if config.testing else "Production"
    print(f"\n---------- Starting {env} ----------\n")
    if len(sys.argv) > 1:
        if sys.argv[1] == "scrappers":
            scrapper_runner.run_scrappers(config)
    else:
        flask_app = create_app(config)
        flask_app.run(host=config.HOST, debug=config.DEBUG, port=config.PORT)
