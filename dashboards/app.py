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

def save_portfolio():
    """Speichert das Portfolio in einer JSON-Datei."""
    portfolio = {
        "btc_amount": st.session_state.btc_amount,
        "eth_amount": st.session_state.eth_amount,
        "ada_amount": st.session_state.ada_amount
    }
    with open(PORTFOLIO_FILE, "w") as file:
        json.dump(portfolio, file)

def load_portfolio():
    """Lädt das Portfolio aus einer JSON-Datei."""
    if os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, "r") as file:
            return json.load(file)
    return {"btc_amount": 0.5, "eth_amount": 2.0, "ada_amount": 100.0}  # Standardwerte

def initialize_session():
    """Initialisiert Session-Variablen mit gespeicherten Werten."""
    saved_portfolio = load_portfolio()
    st.session_state.btc_amount = saved_portfolio["btc_amount"]
    st.session_state.eth_amount = saved_portfolio["eth_amount"]
    st.session_state.ada_amount = saved_portfolio["ada_amount"]

def main():
    st.title("🚀 Crypto Portfolio Tracker")

    # Session State initialisieren
    if "btc_amount" not in st.session_state:
        initialize_session()

    # 📌 Sidebar für Portfolio-Eingabe
    st.sidebar.header("Dein Krypto-Portfolio")
    
    btc = st.sidebar.number_input("Bitcoin (BTC) Menge", min_value=0.0, value=st.session_state.btc_amount, step=0.1)
    eth = st.sidebar.number_input("Ethereum (ETH) Menge", min_value=0.0, value=st.session_state.eth_amount, step=0.1)
    ada = st.sidebar.number_input("Cardano (ADA) Menge", min_value=0.0, value=st.session_state.ada_amount, step=1.0)

    # Werte in Session speichern
    if btc != st.session_state.btc_amount or eth != st.session_state.eth_amount or ada != st.session_state.ada_amount:
        st.session_state.btc_amount = btc
        st.session_state.eth_amount = eth
        st.session_state.ada_amount = ada
        save_portfolio()  # Speichert die Werte dauerhaft

    # 🔄 Live-Preise abrufen
    prices = fetch_crypto_prices()
    
    if prices:
        df = pd.DataFrame(prices).T
        df.columns = ["Preis (USD)"]
        st.write("### 📈 Aktuelle Kryptopreise", df)

        # 📊 Portfolio-Wert berechnen
        portfolio_value = (st.session_state.btc_amount * prices["bitcoin"]["usd"]) + \
                          (st.session_state.eth_amount * prices["ethereum"]["usd"]) + \
                          (st.session_state.ada_amount * prices["cardano"]["usd"])

        st.write(f"### 💰 Dein Portfolio-Wert: **${portfolio_value:,.2f}**")

        # 📉 Historische Preisverläufe abrufen
        btc_data = fetch_historical_prices("bitcoin")
        eth_data = fetch_historical_prices("ethereum")
        ada_data = fetch_historical_prices("cardano")

        if btc_data is not None and eth_data is not None and ada_data is not None:
            # Daten für Plotly vorbereiten
            btc_data["Kryptowährung"] = "Bitcoin"
            eth_data["Kryptowährung"] = "Ethereum"
            ada_data["Kryptowährung"] = "Cardano"

            historical_data = pd.concat([btc_data, eth_data, ada_data])

            # 📈 Preisverlauf zeichnen
            fig = px.line(historical_data, x="date", y="price", color="Kryptowährung",
                          title="📊 Krypto-Preisverläufe der letzten 30 Tage",
                          labels={"date": "Datum", "price": "Preis (USD)", "Kryptowährung": "Kryptowährung"})
            st.plotly_chart(fig)
        
        else:
            st.error("⚠️ Fehler beim Laden der historischen Preisdaten.")

        # 🏆 Risikoanalyse mit Sharpe Ratio & Value at Risk
        example_returns = np.random.normal(0, 0.02, 1000)  # Simulierte Renditen
        sharpe = calculate_sharpe_ratio(pd.Series(example_returns))
        var_95 = calculate_var(example_returns)

        st.write(f"### 📉 Sharpe Ratio: **{sharpe:.2f}**")
        st.write(f"### 🔥 Value at Risk (95%): **{var_95}% Verlust-Wahrscheinlichkeit**")

    else:
        st.error("⚠️ Fehler beim Abrufen der Krypto-Preise von CoinGecko.")

if __name__ == "__main__":
    main()
