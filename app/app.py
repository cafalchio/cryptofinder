from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from app.config_app import TESTING, LOG_FILE
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    if TESTING:
        handler = logging.FileHandler(LOG_FILE)
        app.logger.addHandler(handler)

    with app.app_context():
        db.create_all()
    from app.routes import register_routes

    register_routes(app, db)

    with app.app_context():
        db.create_all()

    migrate = Migrate(app, db)

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=10000)
