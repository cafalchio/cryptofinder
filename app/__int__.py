from app import routes
from flask import Flask
import logging

app = Flask(__name__)

app.logger.setLevel(logging.INFO)
handler = logging.FileHandler("app.log")
app.logger.addHandler(handler)
