from flask import json
from app.app import create_app
from app.config_app import get_logger
import sys

from backend.scrappers import run_scrappers

PORT = 10000
DEBUG = False
HOST = "0.0.0.0"


class ConfigApp:
    def __init__(self, environment="DEV"):
        with open("environment.json") as f:
            self.config = json.loads(f)[environment]


logger = get_logger()

if __name__ == "__main__":
    args = sys.argv
    config = ConfigApp()

    what_to_run = "app"
    if len(args) > 1 and what_to_run == "scrappers":
        what_to_run = "scrappers"
    if what_to_run == "app":
        flask_app = create_app(config)
        flask_app.run(host=HOST, debug=DEBUG, port=PORT)
    elif what_to_run == "scrappers":
        run_scrappers(config)
