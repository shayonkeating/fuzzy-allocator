from typing import Dict, List

import pandas as pd
import yfinance as yf

tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]


def download_ticker_data(
    tickers: List[str], period=str, interval=str
) -> Dict[str, pd.DataFrame]:
    """
    Download ticker data
    """
    data: Dict[str, pd.DataFrame] = {}
    for ticker in tickers:
        print(f"Downloading data for {ticker}...")
        data[ticker] = yf.download(ticker, period=period, interval=interval)
    return data


if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]
    data = download_ticker_data(tickers, period="6mo", interval="1d")

    # Print the first few rows of data for each ticker
    for ticker, df in data.items():
        print(f"\n{ticker} data:")
        print(df.head())
