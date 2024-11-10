from flask import json
from app.app import create_app
from app.config_app import get_logger
import sys
from backend.scrappers import run_scrappers

logger = get_logger()


class ConfigApp:
    def __init__(self, environment="DEV"):
        with open("environments.json", "rb") as f:
            self.config = json.loads(f.read())[environment]
            for key, value in self.config.items():
                setattr(self, key, value )



if __name__ == "__main__":
    args = sys.argv
    config = ConfigApp()
    env = "Development" if config.testing else "Production"
    print(f"\n------ Starting {env} ----------\n")
    what_to_run = "app"
    if len(args) > 1 and what_to_run == "scrappers":
        what_to_run = "scrappers"
    if what_to_run == "app":
        flask_app = create_app(config)
        flask_app.run(host=config.HOST, debug=config.DEBUG, port=config.PORT)
    elif what_to_run == "scrappers":
        run_scrappers(config)
