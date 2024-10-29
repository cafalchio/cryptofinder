from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask import render_template
import pandas as pd
import logging
from backend.data.db import AllCoins, NewCoins
from config_app import (
    NEW_COINS_DETAILS, ALL_COINS, NEW_COINS,
    TESTING, LOG_FILE
)


class Base(DeclarativeBase):
    pass

# engine = sqlalchemy.create_engine("mariadb+mariadbconnector://app_user:Password123!@127.0.0.1:3306/company")


db = SQLAlchemy(model_class=Base)


class DataInterface:

    def get_new_coins(self):
        return db.session.execute(db.select(NewCoins).order_by(NewCoins.date))

    def get_all_coins(self):
        return db.session.execute(db.select(AllCoins).order_by(AllCoins.date))

    def get_shitcoins(self):
        return db.session.execute(db.select(NewCoins).filter(NewCoins.is_shit == True))


def create_app():
    app = Flask(__name__)
    app.config["TESTING"] = TESTING
    if TESTING:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
        handler = logging.FileHandler(LOG_FILE)
        app.logger.addHandler(handler)
    data_interface = DataInterface()
    db.init_app(app)

    @app.route("/")
    def new_coins_today():
        # TODO change csv for a database
        new_coins = data_interface.get_new_coins()
        return render_template("new_coins_today.html", coins=new_coins)

    @app.route("/all_coins")
    def all_coins():
        return render_template("all_coins.html", coins=data_interface.get_all_coins())

    # @app.route("/latest_coins")
    # def latest_coins():
    #     return render_template("latest_coins.html", coins=data_interface.get_latest_coins())

    @app.route("/shitcoins")
    def shitcoins():
        return render_template("shitcoins.html", coins=data_interface.get_shitcoins())

    @app.route("/log")
    def log():
        logs = []
        try:
            with open("app.log", "r") as f:
                for i, line in enumerate(f.readlines()):
                    logs.append(f"<p>{i} - {line}</p>")
            return "".join(logs)
        except FileNotFoundError:
            return "log file not found"

    return app


# if __name__ == "__main__":
#     create_app().run(debug=True, port=10000)
# else:
app = create_app()
