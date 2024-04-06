from flask import render_template
from . import app
from .utils import fetch_and_compare_coins


@app.route("/")
def coin_list():
    coins, message = fetch_and_compare_coins()
    return render_template("coins.html", coins=coins, message=message)


@app.route("/log")
def log():
    logs = []
    try:
        with open("./app.log", "r") as f:
            for i, line in enumerate(f.readlines()):
                logs.append(f"<p>{i} - {line}</p>")
        return "".join(logs)
    except FileNotFoundError:
        return "log file not found"
