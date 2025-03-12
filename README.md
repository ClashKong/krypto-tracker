# Crypto Portfolio Tracker

## 📈 Projektbeschreibung
Der **Crypto Portfolio Tracker** ist ein Echtzeit-Tool zur Verfolgung und Analyse eines Krypto-Portfolios. Es hilft Tradern, ihre Investitionen effizient zu verwalten, Risiken zu analysieren und fundierte Entscheidungen zu treffen.

### Warum dieses Tool?
- **Echtzeit-Daten**: Überwachung des aktuellen Marktwerts deines Portfolios.
- **Risikobewertung**: Berechnung der Volatilität und Sharpe Ratio.
- **Benutzerfreundlich**: Interaktive Dashboards mit Streamlit zur Visualisierung.

## 📊 Datenquellen
- **[CoinGecko API](https://www.coingecko.com/en/api)**: Echtzeit-Preisdaten
- **[Binance API](https://binance-docs.github.io/apidocs/spot/en/)**: Marktdaten und Handelsinformationen

## 🛠 Code-Struktur
```
crypto-tracker/
│── data/              # JSON-Speicher für API-Daten
│── src/               # Python-Skripte für API-Abfragen & Berechnungen
│    ├── fetch_data.py # API-Abfrage & Datenverarbeitung
│    ├── analysis.py   # Berechnung der Portfolio-Statistiken
│── dashboards/        # Streamlit-Visualisierungen
│    ├── app.py        # Dashboard zur Darstellung des Portfolios
│── README.md          # Projektbeschreibung & Setup-Anleitung
```

## 🔧 Setup & Installation
### Voraussetzungen
- Python 3.x
- Abhängigkeiten:
```sh
pip install requests pandas streamlit
```

### Starten des Dashboards
```sh
streamlit run dashboards/app.py
```

## 🔄 Funktionen
### 🔄 Live-Preisdaten abrufen
- Verwendung der CoinGecko API zur Echtzeit-Aktualisierung

### 🔢 Risikoanalyse
- Berechnung der **Volatilität** und **Sharpe Ratio** zur Bewertung der Investitionsrisiken

### 🌍 Interaktive Visualisierung
- Streamlit-Dashboard zur Anzeige des Portfolios

## 👨‍💼 Warum ist das wichtig für Recruiter?
FinTech-Unternehmen und Krypto-Startups suchen nach Data Scientists mit Erfahrung in:
- **Finanzdatenanalyse**
- **API-Integration & Datenvisualisierung**
- **Risikomanagement-Algorithmen**

Dieses Projekt demonstriert deine Fähigkeiten in diesen Bereichen und macht dich für potenzielle Arbeitgeber in **San Francisco** sichtbar!

---
## 🏆 Nächste Schritte
- Implementierung der **CoinGecko API** für Live-Daten ✅
- Berechnung der **Sharpe Ratio** ✅
- Erstellung eines **Streamlit-Dashboards** ✅

