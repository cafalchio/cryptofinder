import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging


db = SQLAlchemy()
migrate = Migrate()

def create_app(config=None):
    if config is None:
        config = ConfigApp("DEV", "../environments.json")
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.testing
    app.config["TESTING"] = config.testing
    db.init_app(app)

    with app.app_context():
        db.create_all()
    from app.routes import register_routes

    register_routes(app, db, config)

    migrate.init_app(app, db)
    logger = get_logger(config.testing)
    logger.info(migrate)

    return app


class ConfigApp:
    def __init__(self, environment="DEV", config_file="environments.json"):
        with open(config_file, "rb") as f:
            env = json.loads(f.read())[environment]
            for key, value in env.items():
                setattr(self, key, value)


def get_logger(testing=False):
    if testing:
        logging.basicConfig(
            format="%(asctime)s-%(name)s-%(levelname)s - %(message)s",
            datefmt="%H:%M:%S",
            level=logging.INFO,
        )
    else:
        logging.basicConfig(
            filename="app.log",
            filemode="a",
            format="%(asctime)s-%(name)s-%(levelname)s - %(message)s",
            datefmt="%H:%M:%S",
            level=logging.INFO,
        )
    return logging.getLogger("cryptofinder")
