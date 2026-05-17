"""
data_fetcher.py
---------------
Handles all data retrieval from Yahoo Finance via yfinance.
Returns clean, validated DataFrames ready for anomaly detection.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def fetch_stock_data(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "1d",
) -> pd.DataFrame:
    """
    Download OHLCV data for a given ticker and date range.

    Parameters
    ----------
    ticker      : Stock symbol, e.g. "AAPL", "TSLA"
    start_date  : ISO date string "YYYY-MM-DD"
    end_date    : ISO date string "YYYY-MM-DD"
    interval    : yfinance interval — "1d", "1h", "30m", etc.

    Returns
    -------
    pd.DataFrame with columns:
        Open, High, Low, Close, Volume, Daily_Return, Price_Range
    Raises ValueError if the ticker is invalid or no data is returned.
    """

    raw = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        interval=interval,
        auto_adjust=True,   # adjusts for splits/dividends automatically
        progress=False,     # suppress yfinance console output
    )

    if raw.empty:
        raise ValueError(
            f"No data returned for '{ticker}' between {start_date} and {end_date}. "
            "Check the ticker symbol and date range."
        )

    # Flatten MultiIndex columns that yfinance sometimes produces
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)

    # Keep only the core OHLCV columns we need
    df = raw[["Open", "High", "Low", "Close", "Volume"]].copy()

    # ── Derived features used by the anomaly detectors ──────────────────────
    # Daily return: percentage change in closing price
    df["Daily_Return"] = df["Close"].pct_change() * 100

    # Intraday price range: how wide the candle is relative to the open
    df["Price_Range"] = (df["High"] - df["Low"]) / df["Open"] * 100

    # Drop the very first row which has NaN from pct_change
    df.dropna(inplace=True)

    # Ensure the index is a proper DatetimeIndex
    df.index = pd.to_datetime(df.index)
    df.index.name = "Date"

    return df


def get_ticker_info(ticker: str) -> dict:
    """
    Fetch basic metadata for a ticker (company name, sector, currency, etc.).
    Returns an empty dict if the lookup fails — callers should handle gracefully.
    """
    try:
        info = yf.Ticker(ticker).info
        return {
            "name":     info.get("longName", ticker),
            "sector":   info.get("sector", "N/A"),
            "currency": info.get("currency", "USD"),
            "exchange": info.get("exchange", "N/A"),
        }
    except Exception:
        return {"name": ticker, "sector": "N/A", "currency": "USD", "exchange": "N/A"}


def validate_date_range(start_date: str, end_date: str) -> None:
    """
    Raise ValueError if the date range is logically invalid.
    Called by the Streamlit app before hitting the API.
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end   = datetime.strptime(end_date,   "%Y-%m-%d")

    if end <= start:
        raise ValueError("End date must be after start date.")

    if (end - start).days < 30:
        raise ValueError("Please select at least 30 days of data for meaningful anomaly detection.")

    if end > datetime.today():
        raise ValueError("End date cannot be in the future.")
