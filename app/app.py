from threading import Thread
from flask import Flask
import logging
from flask import app, render_template
from scheduler import start_scheduler
from utils import fetch_and_compare_coins

app = Flask(__name__)

app.logger.setLevel(logging.INFO)
handler = logging.FileHandler("app.log")
app.logger.addHandler(handler)


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


if __name__ == "__main__":
    scheduler_thread = Thread(target=start_scheduler)
    scheduler_thread.start()
    app.run(debug=True)
