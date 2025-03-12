import requests
import pandas as pd
import streamlit as st
import time
import random

@st.cache_data(ttl=60)  
def fetch_crypto_prices():
    """Holt die aktuellen Krypto-Preise von CoinGecko."""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,cardano,solana,dogecoin,binancecoin",
        "vs_currencies": "usd"
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        if not data:
            raise ValueError("Leere API-Antwort erhalten.")
        return data
    except requests.exceptions.RequestException as e:
        print(f"⚠️ API-Fehler: {e}")
        return None

@st.cache_data(ttl=600)  # Cache für 10 Minuten
def fetch_historical_prices():
    """Holt historische Preise der letzten 30 Tage für alle Coins und reduziert API-Fehler."""
    
    coins = ["bitcoin", "ethereum", "cardano", "solana", "dogecoin", "binancecoin"]
    historical_data = {}

    for coin in coins:
        url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
        params = {
            "vs_currency": "usd",
            "days": "30",
            "interval": "daily"
        }

        retries = 7  # Mehr Versuche für bessere Erfolgsrate
        wait_time = random.uniform(2, 4)  # Starte mit zufälliger Wartezeit (2-4 Sekunden)

        for attempt in range(retries):
            try:
                response = requests.get(url, params=params, timeout=5)
                response.raise_for_status()
                data = response.json()

                if "prices" in data:
                    df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
                    df["date"] = pd.to_datetime(df["timestamp"], unit="ms").dt.date
                    historical_data[coin] = df[["date", "price"]]
                    break  # Erfolgreich! Keine weiteren Versuche nötig
                
            except requests.exceptions.RequestException as e:
                print(f"⚠️ API-Fehler für {coin}, Versuch {attempt+1}/{retries}: {e}")
                wait_time = min(wait_time * 1.5, 10)  # Wartezeit erhöhen, aber maximal 10 Sek.
                time.sleep(wait_time + random.uniform(1, 3))  # Zufällige Zusatzwartezeit
        
        if coin not in historical_data:
            print(f"❌ Konnte Daten für {coin} nach {retries} Versuchen nicht abrufen. Überspringe Coin!")

    return historical_data if historical_data else None