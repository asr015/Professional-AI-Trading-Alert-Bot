"""
risk_calculator.py
Live price history se ATR (Average True Range - ek volatility measure) nikal kar
Entry, Stoploss, Target1, Target2 aur Risk:Reward ratio calculate karta hai.

Logic (industry-standard ATR-based approach):
  - ATR batata hai stock normally ek din me kitna move karta hai
  - Stoploss = Entry -/+ (1 x ATR)   -> itna move "normal noise" hai, isse zyada
    gaya matlab trade galat direction me ja raha hai
  - Target 1 = Entry +/- (1.5 x ATR)  -> conservative target
  - Target 2 = Entry +/- (2.5 x ATR)  -> aggressive target
  - Risk:Reward = (Target1 - Entry) / (Entry - Stoploss)

DISCLAIMER: ATR ek statistical estimate hai, guarantee nahi. Actual market
move news ke sentiment, overall market mood, aur liquidity pe depend karta hai.
"""
import pandas as pd
from price_fetcher import get_price_history


def calculate_atr(price_data: pd.DataFrame, period: int = 14) -> float | None:
    """
    True Range aur ATR calculate karta hai.
    True Range = max(high-low, |high-prev_close|, |low-prev_close|)
    ATR = last `period` din ka True Range ka average
    """
    if price_data.empty or len(price_data) < period + 1:
        return None

    high = price_data["High"]
    low = price_data["Low"]
    close = price_data["Close"]
    prev_close = close.shift(1)

    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    atr = true_range.rolling(window=period).mean().iloc[-1]
    if pd.isna(atr):
        return None
    return round(float(atr), 2)


def calculate_trade_levels(symbol: str, direction: str) -> dict | None:
    """
    Poora trade plan banata hai: entry, stoploss, targets, risk-reward ratio.
    Returns None agar price data na mile (naya listed stock, ya fetch fail ho jaye)
    """
    price_data = get_price_history(symbol, period="2mo", interval="1d")
    if price_data.empty:
        return None

    atr = calculate_atr(price_data)
    if atr is None or atr <= 0:
        return None

    entry = round(float(price_data["Close"].iloc[-1]), 2)

    if direction == "BUY":
        stoploss = round(entry - atr, 2)
        target1 = round(entry + (1.5 * atr), 2)
        target2 = round(entry + (2.5 * atr), 2)
    else:  # SELL
        stoploss = round(entry + atr, 2)
        target1 = round(entry - (1.5 * atr), 2)
        target2 = round(entry - (2.5 * atr), 2)

    risk = abs(entry - stoploss)
    reward = abs(target1 - entry)
    risk_reward_ratio = round(reward / risk, 2) if risk > 0 else 0

    return {
        "entry": entry,
        "stoploss": stoploss,
        "target1": target1,
        "target2": target2,
        "atr": atr,
        "risk_reward_ratio": risk_reward_ratio,
    }


if __name__ == "__main__":
    print(calculate_trade_levels("RELIANCE", "BUY"))
