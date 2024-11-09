import os
from dotenv import load_dotenv
import logging

load_dotenv("./prod.env")
dir_path = os.path.dirname(os.path.abspath(__file__))

# Hours, days, weeks that the new coins w# Get the list of AllCoinsill be showing before it stops to be displayed
DAYS = 1

TESTING = os.getenv("APP_TESTING") == "true"
LOG_FILE = os.getenv("LOG_FILE")
DATABASE = os.getenv("DATABASE")
SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
COINGECKO_API = os.getenv("COINGECKO_API")
ALL_COINS = os.path.join(dir_path, "all_coins.csv")
NEW_COINS = os.path.join(dir_path, "new_coins.csv")
NEW_COINS_DETAILS = os.path.join(dir_path, "new_coins_details.csv")


def get_logger(testing=TESTING):
    if testing:
        logging.basicConfig(
            format="%(asctime)s-%(name)s-%(levelname)s - %(message)s",
            datefmt="%H:%M:%S",
            level=logging.INFO,
        )
    else:
        logging.basicConfig(
            filename=LOG_FILE,
            filemode="a",
            format="%(asctime)s-%(name)s-%(levelname)s - %(message)s",
            datefmt="%H:%M:%S",
            level=logging.INFO,
        )
    return logging.getLogger("cryptofinder")
