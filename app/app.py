from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config_app import get_logger
from sqlalchemy.orm import DeclarativeBase

logger = get_logger()


db = SQLAlchemy()


def create_app(config):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.TESTING
    app.config["TESTING"] = config.TESTING
    db.init_app(app)

    with app.app_context():
        db.create_all()
    from app.routes import register_routes

    register_routes(app, db)

    migrate = Migrate(app, db)
    logger.info(migrate)

    return app
