from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt
import pandas as pd
import numpy as np

import argparse

# python finance/experimental/vol_surface.py --ticker aapl --days 90 (optional)

def option_chains(ticker):
    asset = yf.Ticker(ticker)
    expirations = asset.options
    chains = pd.DataFrame()
    for expiration in expirations:
        opt = asset.option_chain(expiration)
        calls = opt.calls
        calls['optionType'] = "call"
        puts = opt.puts
        puts['optionType'] = "put"
        chain = pd.concat([calls, puts])
        chain['expiration'] = pd.to_datetime(expiration) +\
            pd.DateOffset(hours=23, minutes=59, seconds=59)
        chains = pd.concat([chains, chain])
    chains["daysToExpiration"] =\
        (chains.expiration - dt.datetime.today()).dt.days + 1
    return chains

def solve_laplacian(surface, tol=1e-4, max_iter=2000, zero_thresh=1e-8):
    arr = surface.values.copy()
    fixed_mask = np.abs(arr) >= zero_thresh
    rows, cols = arr.shape
    for iter in range(max_iter):
        old = arr.copy()
        for i in range(rows):
            for j in range(cols):
                if not fixed_mask[i, j]:
                    neighbors = []
                    if i > 0:
                        neighbors.append(arr[i-1, j])
                    if i < rows-1:
                        neighbors.append(arr[i+1, j])
                    if j > 0:
                        neighbors.append(arr[i, j-1])
                    if j < cols-1:
                        neighbors.append(arr[i, j+1])
                    arr[i, j] = np.mean(neighbors)
        arr[fixed_mask] = old[fixed_mask]
        if np.linalg.norm(arr - old, ord=np.inf) < tol:
            break
    result = arr.copy()
    return pd.DataFrame(result, index=surface.index, columns=surface.columns)

def nan_density(df):
    nan_count = df.isna().sum().sum()
    total = df.size
    density = nan_count / total
    return nan_count, total, density

def main():
    parser = argparse.ArgumentParser(
        description="Plot option volatility surface"
    )
    parser.add_argument(
        "--ticker",
        type=str,
        required=True,
        help="Ticker symbol (e.g. AJG)"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=90,
        help="Maximum days to expiration"
    )
    args = parser.parse_args()

    ticker = args.ticker.upper()
    max_days = args.days

    calls = option_chains(ticker)
    filtered = calls[calls['daysToExpiration'] <= max_days]
    surface = filtered.pivot_table(
        values='impliedVolatility',
        index='strike',
        columns='daysToExpiration',
        aggfunc='mean'
    )
    surface_filled = surface.copy().fillna(0.0)

    _, _, bad_dense = nan_density(surface)

    surface = solve_laplacian(surface_filled)
    x, y, z = surface.columns.values, surface.index.values, surface.values
    X, Y = np.meshgrid(x, y)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('Days to expiration')
    ax.set_ylabel('Strike price')
    ax.set_zlabel('Implied volatility')
    # Ticker and percentage of known data used to render
    ax.set_title(
        f"Call implied volatility surface: {ticker}, "
        f"δ data-good: {100 * (1-bad_dense):.2f}%"
    )

    surf = ax.plot_surface(X, Y, z, cmap='coolwarm', edgecolor='none')
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=8)
    plt.show()

if __name__ == "__main__":
    main()
