import pandas as pd

def calculate_sharpe_ratio(returns, risk_free_rate=0.01):
    mean_return = returns.mean()
    std_dev = returns.std()
    if std_dev == 0:
        return 0
    return (mean_return - risk_free_rate) / std_dev
