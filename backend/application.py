import json
import logging
import pandas as pd
from fastapi import FastAPI
import uvicorn
from starlette.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from data import convert_df_dict

logger = logging.getLogger(__name__)
ALL_COINS = "static/all_coins.csv"
NEW_COINS = "static/new_coins.csv"
NEW_COINS_DETAILS = "static/new_coins_details.csv"

logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="%(asctime)s-%(name)s-%(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

app = FastAPI(debug=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/all_coins")
async def root():
    coins = pd.read_csv(ALL_COINS)
    return JSONResponse(content=coins.to_json(orient="records"), status_code=200)


@app.get("/new_coins")
async def root():
    coins = pd.read_csv(NEW_COINS)
    return JSONResponse(content=coins.to_json(orient="records"), status_code=200)


@app.get("/new_coins_detail")
async def root():
    coins = pd.read_csv(NEW_COINS_DETAILS)
    return JSONResponse(content=coins.to_json(orient="records"), status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
