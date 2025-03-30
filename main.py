from fuzzy_allocator.fetch_historical_data import download_ticker_data

tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]
data = download_ticker_data(tickers, period="6mo", interval="1h")

# Print the first few rows of data for each ticker
for ticker, df in data.items():
    print(f"\n{ticker} data:")
    print(df.head())
