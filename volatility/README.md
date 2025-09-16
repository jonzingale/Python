# Option Volatility Surface Plotter

This script fetches options data for a specified stock ticker,
constructs a volatility surface from the implied volatility across strikes
and expiration dates, and visualizes the surface in 3D using matplotlib.

## Features

- Downloads options chains for a valid stock ticker (using Yahoo Finance).
- Filters data by maximum days to expiration.
- Fills missing implied volatilities using a Laplacian smoother for a continuous surface.
- Interactive 3D plot of implied volatility by strike and days to expiration.

## Requirements

- Python 3.7+
- Packages:
  - yfinance
  - pandas
  - numpy
  - matplotlib

Install dependencies (if needed):
```bash
pip install yfinance pandas numpy matplotlib
```

## Usage

Run from the command line:

```bash
python vol_surface.py --ticker TICKER [--days MAX_DAYS]
```
- `--ticker`: Stock symbol (required), e.g., AAPL, AJG.
- `--days`: Maximum days to expiration to include (optional, default is 90).

### Examples

Plot Apple's volatility surface for options expiring in the next 100 days:
```bash
python vol_surface.py --ticker AAPL --days 100
```

Plot Gallagher's (AJG) volatility surface for the default window:
```bash
python vol_surface.py --ticker AJG
```

## How It Works

1. **Option Data Fetch:** Downloads all available calls and puts for the ticker.
2. **Data Filtering:** Includes only contracts with days to expiration ≤ specified maximum.
3. **Volatility Surface:** Creates a pivot table of implied volatility by strike and expiration.
4. **Laplacian Smoothing:** Applies a Laplacian solver to fill gaps in the data grid.
5. **Visualization:** Renders a 3D surface plot using matplotlib.
