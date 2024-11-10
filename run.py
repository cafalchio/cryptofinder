from flask import json
from app.app import create_app
from app.config_app import get_logger
import sys
from backend.scrappers import scrapper_runner

logger = get_logger()


class ConfigApp:
    def __init__(self, environment="DEV"):
        with open("environments.json", "rb") as f:
            env = json.loads(f.read())[environment]
            for key, value in env.items():
                setattr(self, key, value)


if __name__ == "__main__":
    config = ConfigApp()
    env = "Development" if config.testing else "Production"
    print(f"\n------ Starting {env} ----------\n")
    if len(sys.argv) > 1:
        if sys.argv[1] == "scrappers":
            scrapper_runner.run_scrappers(config)
    else:
        flask_app = create_app(config)
        flask_app.run(host=config.HOST, debug=config.DEBUG, port=config.PORT)
