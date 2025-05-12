import os

import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from typing import List

from fastapi.responses import HTMLResponse, Response

app = FastAPI()
load_dotenv()

def get_crypto_currency(currencies: List[str]):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(currencies)}&vs_currencies=usd"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {"error": "Failed to fetch data from CoinGecko"}

@app.get("/crypto", response_class=HTMLResponse)
async def get_currencies(currencies: List[str] = Query(...)):
    data = get_crypto_currency(currencies)

    if "error" in data:
        return f"<h1>Error</h1><h2>{data['error']}</h2>"

    html = "<h1>Crypto Prices (USD)</h1>"
    for coin, info in data.items():
        html += f"<h2>{coin.title()}: ${info['usd']}</h2>"
    return html

@app.get("/moodle", response_class=HTMLResponse)
async def get_moodle_info(login: str):
    if login == os.getenv("MOODLE_LOGIN"):
        html = "<h1>MOODLE INFO </h1>"
        html+= f"<h2>Name = {os.getenv('MOODLE_NAME')}</h2>"
        html+= f"<h2>Surname = {os.getenv('MOODLE_SURNAME')}</h2>"
        html+= f"<h2>Group = {os.getenv('MOODLE_GROUP')}</h2>"
        html+= f"<h2>Course = {os.getenv('MOODLE_COURSE')}</h2>"
        return HTMLResponse(content=html)
    else:
        error = f"<h1>Invalid login</h1><h2>{login}</h2>"
        return HTMLResponse(content=error)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)