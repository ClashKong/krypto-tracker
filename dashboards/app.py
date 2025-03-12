import streamlit as st
import pandas as pd
import plotly.express as px
from src.fetch_data import fetch_crypto_prices, fetch_historical_prices
from src.analysis import calculate_sharpe_ratio, calculate_var
import numpy as np
import sys
import os

# Sicherstellen, dass src als Modul erkannt wird
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def initialize_session():
    """Initialisiert die Session-Variablen, falls sie nicht existieren."""
    if "btc_amount" not in st.session_state:
        st.session_state.btc_amount = 0.5
    if "eth_amount" not in st.session_state:
        st.session_state.eth_amount = 2.0
    if "ada_amount" not in st.session_state:
        st.session_state.ada_amount = 100.0

def main():
    st.title("🚀 Crypto Portfolio Tracker")

    # Session State initialisieren
    initialize_session()

    # 📌 Sidebar für Portfolio-Eingabe
    st.sidebar.header("Dein Krypto-Portfolio")
    
    st.session_state.btc_amount = st.sidebar.number_input("Bitcoin (BTC) Menge", min_value=0.0, value=st.session_state.btc_amount, step=0.1)
    st.session_state.eth_amount = st.sidebar.number_input("Ethereum (ETH) Menge", min_value=0.0, value=st.session_state.eth_amount, step=0.1)
    st.session_state.ada_amount = st.sidebar.number_input("Cardano (ADA) Menge", min_value=0.0, value=st.session_state.ada_amount, step=1.0)

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
