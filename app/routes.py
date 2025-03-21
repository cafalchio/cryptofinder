from flask import render_template
from backend.data.models import AllCoins
from datetime import datetime, timedelta
from sqlalchemy import desc


def register_routes(app, db, config):
    time_delta = timedelta(days=int(config.NEW_COINS_INTERVAL))
    today = datetime.now().date()
    cut_off_days = today - time_delta

    @app.route("/")
    def new_coins_today():
        result = db.session.execute(
            db.select(AllCoins)
            .filter(AllCoins.added > cut_off_days)
            .order_by(desc(AllCoins.added))
        )
        new_coins = result.scalars().all()

        for coin in new_coins:
            coin.added = coin.added.strftime("%Y-%b-%d")

        return render_template("new_coins_today.html", coins=new_coins)

    @app.route("/all_coins")
    def all_coins():
        result = db.session.execute(db.select(AllCoins).order_by(AllCoins.added))
        all_coins = result.scalars().all()
        for coin in all_coins:
            coin.added = coin.added.strftime("%Y-%m-%d")
        return render_template("all_coins.html", coins=all_coins)

    @app.route("/shitcoins")
    def shitcoins():
        result = db.session.execute(db.select(AllCoins).filter(AllCoins.is_shit))
        # Get the list of AllCoins that are "shitcoins"
        shitcoins = result.scalars().all()
        return render_template("shitcoins.html", coins=shitcoins)

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
