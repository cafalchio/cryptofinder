from flask import Flask
import logging
from flask import render_template
import pandas as pd

logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="%(asctime)s-%(name)s-%(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

logging.info("Running Cryptofinder")

logger = logging.getLogger("cryptofinder")

ALL_COINS = "/home/cafalchio/Projects/cryptofinder/app/all_coins.csv"
NEW_COINS = "/home/cafalchio/Projects/cryptofinder/app/new_coins.csv"
NEW_COINS_DETAILS = "/home/cafalchio/Projects/cryptofinder/app/new_coins_details.csv"


def create_app():
    app = Flask(__name__)

    app.logger.setLevel(logging.INFO)
    handler = logging.FileHandler("app.log")
    app.logger.addHandler(handler)

    @app.route("/")
    def new_coins_today():
        new_coins_df = pd.read_csv(NEW_COINS)
        if len(new_coins_df) > 0:
            message = "New coins found!"
        else:
            message = "No new coins found"
        new_coins = new_coins_df.to_dict(
            "records") if not new_coins_df.empty else []
        return render_template("new_coins_today.html", coins=new_coins, message=message)

    @app.route("/all_coins")
    def all_coins():
        all_coins_df = pd.read_csv(ALL_COINS)

        all_coins = all_coins_df.to_dict(
            "records") if not all_coins_df.empty else []

        return render_template("all_coins.html", coins=all_coins)

    @app.route("/latest_coins")
    def latest_coins():
        latest_coins_df = pd.read_csv(NEW_COINS_DETAILS)

        coins = latest_coins_df.to_dict(
            "records") if not latest_coins_df.empty else []

        return render_template("latest_coins.html", coins=coins)

    @app.route("/shitcoins")
    def shitcoins():
        return render_template("shitcoins.html")

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


if __name__ == "__main__":
    # scheduler_thread = Thread(target=start_scheduler)
    # scheduler_thread.start()
    create_app().run(debug=True)
else:
    gunicorn_app = create_app()
