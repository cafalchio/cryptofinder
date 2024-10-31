from flask import render_template
from backend.data.models import AllCoins, NewCoins


def register_routes(app, db):

    @app.route("/")
    def new_coins_today():
        result = db.session.execute(
            db.select(NewCoins).order_by(NewCoins.added)
        )
        new_coins = result.scalars().all()  # Get the list of NewCoins
        return render_template("new_coins_today.html", coins=new_coins)

    @app.route("/all_coins")
    def all_coins():
        result = db.session.execute(
            db.select(AllCoins).order_by(AllCoins.added)
        )
        all_coins = result.scalars().all()  # Get the list of AllCoins
        return render_template("all_coins.html", coins=all_coins)

    @app.route("/shitcoins")
    def shitcoins():
        result = db.session.execute(
            db.select(NewCoins).filter(NewCoins.is_shit == True)
        )
        # Get the list of NewCoins that are "shitcoins"
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
        
