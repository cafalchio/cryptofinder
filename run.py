from app.app import create_app, ConfigApp
import sys
from backend import scrappers

CONFIG_FILE = "environments.json"


def config_app(env):
    config = ConfigApp(environment=env, config_file=CONFIG_FILE)
    flask_app = create_app(config)
    return flask_app, config


# Initialize the app
env = "DEV" if "dev" in sys.argv else "PROD"

if env == "PROD":
    flask_app, config = config_app("PROD")
else:
    flask_app, config = config_app("DEV")
    print(f"{config.HOST}:{config.PORT} - DEBUG: {config.DEBUG}")

app = flask_app

if __name__ == "__main__":
    flask_app.run(host=config.HOST, debug=config.DEBUG, port=config.PORT)
