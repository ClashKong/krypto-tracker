import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from src.fetch_data import fetch_crypto_prices, fetch_historical_prices
from src.analysis import calculate_sharpe_ratio, calculate_var
import numpy as np
import sys

# Sicherstellen, dass src als Modul erkannt wird
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

PORTFOLIO_FILE = "data/portfolio.json"
COINS = ["bitcoin", "ethereum", "cardano", "solana", "dogecoin", "binancecoin"]

def save_portfolio():
    """Speichert das Portfolio in einer JSON-Datei."""
    portfolio = {coin: st.session_state[coin] for coin in COINS}
    with open(PORTFOLIO_FILE, "w") as file:
        json.dump(portfolio, file)

def load_portfolio():
    """Lädt das Portfolio aus einer JSON-Datei & erstellt sie neu, falls sie leer ist."""
    default_portfolio = {coin: 0.0 for coin in COINS}  # Standardwerte (0 Coins)

    if os.path.exists(PORTFOLIO_FILE):
        try:
            with open(PORTFOLIO_FILE, "r") as file:
                saved_portfolio = json.load(file)

            # Sicherstellen, dass alle Coins existieren (falls alte Datei unvollständig ist)
            for coin in COINS:
                if coin not in saved_portfolio:
                    saved_portfolio[coin] = 0.0

            return saved_portfolio

        except json.JSONDecodeError:
            # Falls die Datei leer oder beschädigt ist, neu schreiben
            with open(PORTFOLIO_FILE, "w") as file:
                json.dump(default_portfolio, file)
            return default_portfolio

    return default_portfolio  # Falls Datei nicht existiert

def initialize_session():
    """Initialisiert Session-Variablen mit gespeicherten Werten."""
    saved_portfolio = load_portfolio()
    for coin in COINS:
        if coin not in st.session_state:
            st.session_state[coin] = saved_portfolio[coin]

def main():
    st.title("🚀 Crypto Portfolio Tracker")

    # Session State initialisieren
    if COINS[0] not in st.session_state:
        initialize_session()

    # 📌 Sidebar für Portfolio-Eingabe
    st.sidebar.header("Dein Krypto-Portfolio")
    
    for coin in COINS:
        st.session_state[coin] = st.sidebar.number_input(
            f"{coin.capitalize()} (Menge)", min_value=0.0, value=st.session_state[coin], step=0.1
        )

    # Speichert die Werte nur, wenn sie sich ändern
    if any(st.session_state[coin] != load_portfolio()[coin] for coin in COINS):
        save_portfolio()

    # 🔄 Live-Preise abrufen
    prices = fetch_crypto_prices()
    
    if prices:
        df = pd.DataFrame(prices).T
        df.columns = ["Preis (USD)"]
        st.write("### 📈 Aktuelle Kryptopreise", df)

        # DEBUG: Alle Preise anzeigen
        st.write("🔍 DEBUG: Live-Preise von CoinGecko", prices)

        # 📊 Portfolio-Wert berechnen (jetzt mit allen Coins!)
        portfolio_value = 0
        for coin in COINS:
            if coin in prices:
                st.write(f"✅ {coin}: {st.session_state[coin]} x {prices[coin]['usd']} USD")  # Debug-Ausgabe
                portfolio_value += st.session_state[coin] * prices[coin]["usd"]
            else:
                st.write(f"⚠️ Kein Preis für {coin} gefunden!")  # Warnung, falls ein Preis fehlt

        st.write(f"### 💰 Dein Portfolio-Wert: **${portfolio_value:,.2f}**")

        # 📉 Historische Preisverläufe abrufen
        historical_data = []
        for coin in COINS:
            data = fetch_historical_prices(coin)
            if data is not None:
                data["Kryptowährung"] = coin.capitalize()
                historical_data.append(data)

        if historical_data:
            df_hist = pd.concat(historical_data)

            # 📈 Preisverlauf zeichnen
            fig = px.line(df_hist, x="date", y="price", color="Kryptowährung",
                          title="📊 Krypto-Preisverläufe der letzten 30 Tage",
                          labels={"date": "Datum", "price": "Preis (USD)", "Kryptowährung": "Kryptowährung"})
            st.plotly_chart(fig)
        
        else:
            st.error("⚠️ Fehler beim Laden der historischen Preisdaten.")

        # 📊 Trading-Strategien: HODL vs. Dollar Cost Averaging (DCA)
        st.write("## 📊 Trading-Strategien: HODL vs. Dollar Cost Averaging (DCA)")

        hodl_value = portfolio_value
        dca_value = hodl_value * 1.05  

        strategy_df = pd.DataFrame({"Strategie": ["HODL", "DCA"], "Wert (USD)": [hodl_value, dca_value]})
        st.bar_chart(strategy_df.set_index("Strategie"))

        # 🏆 Risikoanalyse mit Sharpe Ratio & Value at Risk
        example_returns = np.random.normal(0, 0.02, 1000)
        sharpe = calculate_sharpe_ratio(pd.Series(example_returns))
        var_95 = calculate_var(example_returns)

        st.write(f"### 📉 Sharpe Ratio: **{sharpe:.2f}**")
        st.write(f"### 🔥 Value at Risk (95%): **{var_95}% Verlust-Wahrscheinlichkeit**")

    else:
        st.error("⚠️ Fehler beim Abrufen der Krypto-Preise von CoinGecko.")

if __name__ == "__main__":
    main()
