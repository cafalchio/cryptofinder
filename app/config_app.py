import os
from dotenv import load_dotenv
import logging

load_dotenv()

TESTING = os.getenv("APP_TESTING") == "true"
LOG_FILE = os.getenv('LOG_FILE')
DATABASE = os.getenv('FLASK_DATABASE')
SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

if TESTING:
    logging.basicConfig(
        format="%(asctime)s-%(name)s-%(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
        level=logging.DEBUG,
    )
else:
    logging.basicConfig(
        filename=LOG_FILE,
        filemode="a",
        format="%(asctime)s-%(name)s-%(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )
logger = logging.getLogger("cryptofinder")
