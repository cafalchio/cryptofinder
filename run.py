from app.scheduler import start_scheduler
from threading import Thread
from flask import Flask
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
handler = logging.FileHandler("app.log")
app.logger.addHandler(handler)

if __name__ == "__main__":
    scheduler_thread = Thread(target=start_scheduler)
    scheduler_thread.start()
    app.run(debug=True)
