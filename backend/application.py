import logging
import os

from fastapi import FastAPI
import uvicorn

from backend.data.data_interface import Interface

current_dir = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger(__name__)

logging.basicConfig(
    filename="logs/app.log",
    filemode="a",
    format="%(asctime)s-%(name)s-%(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

app = FastAPI(debug=True)
interface = Interface()

@app.get("/all_coins")
async def root():
    return interface.all_coins


@app.get("/new_coins")
async def root():
    return interface.new_coins


@app.get("/new_coins_details")
async def root():
    return interface.new_coins_details


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
