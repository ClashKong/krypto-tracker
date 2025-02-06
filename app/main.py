from fastapi import FastAPI
import requests

app = FastAPI()

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

@app.get("/crypto/{symbol}")
def get_crypto_price(symbol: str, currency: str = "chf"):
    params = {
        "ids": symbol.lower(),
        "vs_currencies": currency.lower()
    }
    response = requests.get(COINGECKO_API_URL, params=params)
    
    if response.status_code != 200:
        return {"error": "Fehler beim Abrufen der Daten"}
    
    data = response.json()
    return {symbol: data.get(symbol.lower(), "Nicht gefunden")}

