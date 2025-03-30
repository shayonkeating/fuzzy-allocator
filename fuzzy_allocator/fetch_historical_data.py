import yfinance as yf

tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]
data = {}

for ticker in tickers:
    # Fetching 6 months of daily data
    data[ticker] = yf.download(ticker, period="6mo", interval="1d")
