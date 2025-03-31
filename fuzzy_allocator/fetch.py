from typing import List

import pandas as pd

from fuzzy_allocator.fetch_historical_data import download_ticker_data
from fuzzy_allocator.trading_funcs import (
    compute_bb_percentile,
    compute_ema_trend,
    compute_pmarp,
)


def generate_take_profit_signal(
    pmarp_percentile: float,
    standard_threshold: float = 75,
    long_term_threshold: float = 90,
) -> str:
    """
    Generates a take profit signal based on the PMARP percentile.
    """
    if pmarp_percentile >= long_term_threshold:
        return f"Long-term signal: PMARP percentile at {pmarp_percentile:.1f}%. Consider selling (take profit)."
    elif pmarp_percentile >= standard_threshold:
        return f"Standard signal: PMARP percentile at {pmarp_percentile:.1f}%. Potential take profit signal."
    else:
        return f"No take profit signal: PMARP percentile at {pmarp_percentile:.1f}%."


def generate_buy_signal(pmarp_percentile: float, buy_threshold: float = 25) -> str:
    """
    Generates a buy signal based on the PMARP percentile.
    """
    if pmarp_percentile <= buy_threshold:
        return f"Buy signal: PMARP percentile is {pmarp_percentile:.1f}%, which is below the buy threshold of {buy_threshold}%."
    else:
        return f"No buy signal: PMARP percentile is {pmarp_percentile:.1f}% (buy threshold is {buy_threshold}%)."


def generate_final_signal(
    pmarp_percentile: float,
    bb_percentile: float,
    buy_threshold: float = 25,
    sell_threshold: float = 90,
) -> str:
    """
    Generates a final trading signal based on both PMARP and Bollinger Bands percentiles.
    A final signal of "Buy" is returned if both indicators are below the buy threshold,
    "Sell" if both are above the sell threshold, and "Hold" otherwise.
    """
    if pmarp_percentile <= buy_threshold and bb_percentile <= buy_threshold:
        return "Buy"
    elif pmarp_percentile >= sell_threshold and bb_percentile >= sell_threshold:
        return "Sell"
    else:
        return "Hold"


def analyze_ticker(df: pd.DataFrame) -> None:
    """
    Analyzes a ticker's DataFrame and prints the PMARP, Bollinger Bands percentile,
    EMA trend, buy signal, take profit signal, and final signal.
    """
    # Compute PMARP and Bollinger Bands results
    pmarp_results = compute_pmarp(df, ma_period=50, lookback=100)
    bb_results = compute_bb_percentile(df, ma_period=20, lookback=100)

    if pmarp_results:
        current_ratio, pmarp_percentile = pmarp_results
        print(f"[INFO] PMARP: {current_ratio:.4f}, Percentile: {pmarp_percentile:.1f}%")
        tp_signal = generate_take_profit_signal(pmarp_percentile)
        buy_signal = generate_buy_signal(pmarp_percentile, buy_threshold=25)
        print(f"[INFO] {tp_signal}")
        print(f"[INFO] {buy_signal}")
    else:
        print("[ERROR] Insufficient data for PMARP computation.")

    if bb_results:
        current_bb_pos, bb_percentile = bb_results
        print(
            f"[INFO] Bollinger Bands Position: {current_bb_pos:.4f}, Percentile: {bb_percentile:.1f}%"
        )
    else:
        print("[ERROR] Insufficient data for Bollinger Bands percentile computation.")

    # Compute trend using EMAs
    trend = compute_ema_trend(df, short_period=50, long_period=200)
    print(f"[INFO] Trend: {trend}")

    # If both PMARP and Bollinger Bands results are available, generate a final signal.
    if pmarp_results and bb_results:
        final_signal = generate_final_signal(
            pmarp_percentile, bb_percentile, buy_threshold=25, sell_threshold=90
        )
        print(f"[INFO] Final Signal: {final_signal}")


def main(tickers: List[str], period: str, interval: str) -> None:
    data = download_ticker_data(tickers, period, interval)
    for ticker, df in data.items():
        print(f"\n=== {ticker} Analysis ===")
        analyze_ticker(df)


if __name__ == "__main__":
    tickers = [
        "NVDA",
        "COST",
        "META",
        "AMZN",
        "GOOGL",
        "PLTR",
        "CRWD",
        "CMG",
        "PANW",
    ]  # Example: using NVDA for testing
    main(tickers, period="1y", interval="4h")
