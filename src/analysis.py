import numpy as np
import pandas as pd

def calculate_sharpe_ratio(returns, risk_free_rate=0.01):
    """Berechnet die Sharpe Ratio als Risikokennzahl."""
    mean_return = returns.mean()
    std_dev = returns.std()
    if std_dev == 0:
        return 0
    return (mean_return - risk_free_rate) / std_dev

def calculate_var(returns, confidence_level=0.95):
    """Berechnet Value at Risk (VaR) mit Monte-Carlo-Simulation."""
    if len(returns) == 0:
        return 0

    mean_return = np.mean(returns)
    std_dev = np.std(returns)
    
    # Quantil für das gegebene Konfidenzniveau bestimmen
    var_threshold = np.percentile(returns, (1 - confidence_level) * 100)
    
    return round(var_threshold * 100, 2)  # Prozentuale Angabe

# Testlauf
if __name__ == "__main__":
    test_returns = np.random.normal(0, 0.02, 1000)  # 1000 Tage simulierte Renditen
    print(f"📉 Value at Risk (VaR 95%): {calculate_var(test_returns)}%")
