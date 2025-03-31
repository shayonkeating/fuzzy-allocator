from typing import Optional, Tuple

import pandas as pd
from scipy.stats import percentileofscore


def compute_pmarp(
    df: pd.DataFrame, ma_period: int = 50, lookback: int = 100
) -> Optional[Tuple[float, float]]:
    """
    Computes the Price Moving Average Ratio (PMARP) and its percentile.

    PMARP = Current Close / Moving Average over `ma_period` periods.
    The percentile is calculated over the last `lookback` periods.

    Returns:
        Tuple containing:
          - current PMARP value (float)
          - percentile rank (float)
        Returns None if there's insufficient data.
    """
    # Work on a copy of the DataFrame
    df = df.copy()

    # Get the Close column; if it's a DataFrame, squeeze it to a Series.
    close = df["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.squeeze()  # Alternatively: close = close.iloc[:, 0]

    # Calculate the moving average
    ma = close.rolling(window=ma_period).mean()
    df["MA"] = ma

    # Calculate PMARP as the ratio of the close price to the moving average
    df["PMARP"] = close / ma

    # Ensure we have enough data points
    if df["PMARP"].dropna().shape[0] < lookback:
        return None

    historical_ratios = df["PMARP"].dropna().iloc[-lookback:]
    current_ratio = historical_ratios.iloc[-1]
    pmarp_percentile = percentileofscore(historical_ratios, current_ratio)

    return current_ratio, pmarp_percentile


from typing import Optional, Tuple

import pandas as pd
from scipy.stats import percentileofscore


def compute_bb_percentile(
    df: pd.DataFrame, ma_period: int = 20, lookback: int = 100
) -> Optional[Tuple[float, float]]:
    """
    Computes the Bollinger Bands position and its percentile.

    The position is defined as:
      (Close - LowerBand) / (UpperBand - LowerBand)

    where LowerBand = MA - 2*std and UpperBand = MA + 2*std.

    Returns:
        Tuple of the current Bollinger Bands position (0-1) and its percentile rank.
        Returns None if not enough data is available.
    """
    df = df.copy()

    # Ensure the 'Close' column is a Series
    close = df["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.squeeze()  # Alternatively: close = close.iloc[:, 0]

    # Calculate the moving average and standard deviation for Bollinger Bands
    df["MA_bb"] = close.rolling(window=ma_period).mean()
    df["std_bb"] = close.rolling(window=ma_period).std()
    df["UpperBand"] = df["MA_bb"] + 2 * df["std_bb"]
    df["LowerBand"] = df["MA_bb"] - 2 * df["std_bb"]

    # Calculate the position within the Bollinger Bands
    df["BB_Pos"] = (close - df["LowerBand"]) / (df["UpperBand"] - df["LowerBand"])

    if df["BB_Pos"].dropna().shape[0] < lookback:
        return None

    historical_pos = df["BB_Pos"].dropna().iloc[-lookback:]
    current_pos = historical_pos.iloc[-1]
    bb_percentile = percentileofscore(historical_pos, current_pos)

    return current_pos, bb_percentile


def compute_ema_trend(
    df: pd.DataFrame, short_period: int = 50, long_period: int = 200
) -> str:
    """
    Computes short-term and long-term exponential moving averages (EMAs) and returns a trend signal.

    Args:
        df (pd.DataFrame): Historical price data containing at least the 'Close' column.
        short_period (int): The period for the short-term EMA.
        long_period (int): The period for the long-term EMA.

    Returns:
        str: "Uptrend" if the short EMA is above the long EMA,
             "Downtrend" if the short EMA is below the long EMA,
             "Sideways" otherwise.
    """
    # Ensure we work with a Series for Close
    close = df["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.squeeze()

    short_ema = close.ewm(span=short_period, adjust=False).mean()
    long_ema = close.ewm(span=long_period, adjust=False).mean()

    short_last = short_ema.iloc[-1]
    long_last = long_ema.iloc[-1]

    if short_last > long_last:
        return "Uptrend"
    elif short_last < long_last:
        return "Downtrend"
    else:
        return "Sideways"
