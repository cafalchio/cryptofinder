import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config_app import DATABASE, TESTING, get_logger
from sqlalchemy.orm import DeclarativeBase

logger = get_logger()


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def create_app(database=None):
    if database is None:
        database = DATABASE
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = TESTING
    app.config["TESTING"] = TESTING
    db.init_app(app)

    with app.app_context():
        db.create_all()
    from app.routes import register_routes

    register_routes(app, db)

    migrate = Migrate(app, db)
    logger.info(migrate)

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=10000)
