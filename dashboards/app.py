import streamlit as st
import pandas as pd
from src.fetch_data import fetch_crypto_prices
from src.analysis import calculate_sharpe_ratio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def main():
    st.title("Crypto Portfolio Tracker")

    prices = fetch_crypto_prices()
    if prices:
        df = pd.DataFrame(prices).T
        df.columns = ["Price (USD)"]
        st.write("### Aktuelle Kryptopreise", df)
    else:
        st.error("Fehler beim Abrufen der Daten von CoinGecko")

    # Beispiel-Daten für Renditen (normalerweise aus historischen Daten berechnet)
    example_returns = pd.Series([0.02, 0.01, -0.005, 0.03, -0.02])
    sharpe = calculate_sharpe_ratio(example_returns)
    st.write(f"### Sharpe Ratio: {sharpe:.2f}")

if __name__ == "__main__":
    main()
