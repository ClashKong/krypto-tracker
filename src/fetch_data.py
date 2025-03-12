import requests
import pandas as pd
import time

def fetch_crypto_prices():
    """Holt die aktuellen Krypto-Preise von CoinGecko."""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,cardano",
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

def fetch_historical_prices(crypto_id):
    """Holt die historischen Preise der letzten 30 Tage von CoinGecko."""
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "30",
        "interval": "daily"
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # Extrahiert Zeitstempel und Preise
        if "prices" in data:
            df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
            df["date"] = pd.to_datetime(df["timestamp"], unit="ms").dt.date
            return df[["date", "price"]]
        else:
            raise ValueError("Fehlerhafte Datenstruktur von CoinGecko")
    
    except requests.exceptions.RequestException as e:
        print(f"⚠️ API-Fehler für {crypto_id}: {e}")
        return None

# Testlauf, um Daten zu prüfen
if __name__ == "__main__":
    print("🔄 Abrufe aktuelle Preise...")
    print(fetch_crypto_prices())
    
    print("\n📊 Abrufe historische Preise für Bitcoin...")
    print(fetch_historical_prices("bitcoin"))
