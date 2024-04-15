import logging

from fastapi import FastAPI
import uvicorn
from starlette.staticfiles import StaticFiles
from coingecko import Coingecko

logger = logging.getLogger(__name__)

logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="%(asctime)s-%(name)s-%(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/all_coins")
async def root():
    coins = [
        {
            "id": "c1",
            "name": "coin1",
            "symbol": "C1",
            "found": "24-04-08",
            "is_shit": ""
        },
    ]
    return coins


@app.get("/new_coins")
async def root():
    coins = [
        {
            "id": "c1",
            "name": "coin1",
            "symbol": "C1",
            "found": "24-04-08"
        },
    ]
    return coins


@app.get("/shitcoins")
async def root():
    coins = [
        {
            "id": "c1",
            "name": "coin1",
            "symbol": "C1",
            "found": "24-04-08"
        },
    ]
    return coins


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
