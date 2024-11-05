from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config_app import DATABASE, TESTING
from sqlalchemy.orm import DeclarativeBase
import logging

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def create_app(DATABASE):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
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
    create_app(DATABASE).run(debug=True, port=10000)
