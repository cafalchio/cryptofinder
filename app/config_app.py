import os
from dotenv import load_dotenv
import logging

load_dotenv()
dir_path = os.path.dirname(os.path.abspath(__file__))

TESTING = os.getenv("APP_TESTING") == "true"
LOG_FILE = os.getenv('LOG_FILE')
DATABASE = os.getenv('FLASK_DATABASE')
SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
COINGECKO_API = os.getenv('COINGECKO_API')
ALL_COINS = os.path.join(dir_path, "all_coins.csv")
NEW_COINS = os.path.join(dir_path, "new_coins.csv")
NEW_COINS_DETAILS = os.path.join(dir_path, "new_coins_details.csv")

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
