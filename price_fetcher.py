"""
price_fetcher.py
Free live/recent price data - Yahoo Finance (yfinance library) ke through.
NSE stocks ke liye symbol ke aage ".NS" lagta hai (Yahoo Finance convention).
Koi API key nahi chahiye, bilkul free hai.
"""
import yfinance as yf
import pandas as pd


def get_price_history(symbol: str, period: str = "1mo", interval: str = "1d") -> pd.DataFrame:
    """
    NSE symbol ke liye price history laata hai.
    Returns: pandas DataFrame with Open, High, Low, Close, Volume columns (empty if fail ho gaya)
    """
    try:
        yahoo_symbol = f"{symbol}.NS"
        ticker = yf.Ticker(yahoo_symbol)
        data = ticker.history(period=period, interval=interval)
        return data
    except Exception as e:
        print(f"[price_fetcher] {symbol} ka price fetch fail ho gaya: {e}")
        return pd.DataFrame()


def get_latest_price(symbol: str) -> float | None:
    """Sabse latest closing/current price nikalta hai. Fail hone pe None."""
    data = get_price_history(symbol, period="5d", interval="1d")
    if data.empty:
        return None
    return round(float(data["Close"].iloc[-1]), 2)


if __name__ == "__main__":
    price = get_latest_price("RELIANCE")
    print(f"RELIANCE latest price: {price}")
