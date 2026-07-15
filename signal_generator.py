"""
signal_generator.py
Yeh core engine hai - news fetch karta hai, uske andar stock symbol,
sentiment, aur live price levels dhundta hai, aur sirf HIGH PROBABILITY,
HIGH RISK-REWARD signals return karta hai.

"High probability, solid trade" ka matlab yahan:
  1. Stock clearly identify hua ho (naam match ho gaya)
  2. Sentiment direction clear ho (BUY ya SELL, NEUTRAL/MIXED nahi)
  3. Confidence score >= MIN_CONFIDENCE_SCORE (news ki strength, config me set hai)
  4. Live price data available ho (entry/stoploss/target calculate ho sake)
  5. Risk:Reward ratio >= MIN_RISK_REWARD_RATIO (config me set hai, default 1.5)
  6. News fresh ho (already sent na ho, duplicate na ho)

DISCLAIMER: Yeh ek rule-based filter hai, guarantee nahi hai. Market
me hamesha risk rehta hai - koi bhi signal 100% sahi nahi hota.
"""
import json
import os
from news_fetcher import fetch_latest_news
from stock_mapper import find_stocks_in_text
from sentiment_analyzer import analyze_sentiment
from risk_calculator import calculate_trade_levels
from config import MIN_CONFIDENCE_SCORE, MIN_RISK_REWARD_RATIO, CACHE_FILE, MAX_CACHE_SIZE


def _load_sent_cache() -> set:
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()


def _save_sent_cache(cache: set):
    cache_list = list(cache)[-MAX_CACHE_SIZE:]  # sirf recent IDs rakho
    with open(CACHE_FILE, "w") as f:
        json.dump(cache_list, f)


def generate_signals() -> list:
    """
    Latest news scan karke high-probability trade signals return karta hai.
    Returns: list of dicts, har dict ek signal hai:
        {stock, symbol, direction, confidence, reason, news_title, news_link, source}
    """
    sent_cache = _load_sent_cache()
    news_items = fetch_latest_news(max_age_minutes=30)
    signals = []

    for news in news_items:
        if news["id"] in sent_cache:
            continue  # yeh news pehle process ho chuki hai

        full_text = f"{news['title']}. {news['summary']}"

        # Step 1: Stock identify karo
        matched_stocks = find_stocks_in_text(full_text)
        if not matched_stocks:
            continue  # koi known stock mention nahi hai, skip

        # Step 2: Sentiment nikaalo
        sentiment = analyze_sentiment(full_text)
        if sentiment["direction"] == "NEUTRAL":
            continue  # direction clear nahi, skip (high-probability ke liye clarity chahiye)

        # Step 3: Confidence filter
        if sentiment["confidence"] < MIN_CONFIDENCE_SCORE:
            continue

        # Step 4: Har matched stock ke liye trade levels nikaalo aur signal banao
        for stock in matched_stocks:
            trade_levels = calculate_trade_levels(stock["symbol"], sentiment["direction"])

            # Agar price data hi nahi mila (illiquid/new stock), signal skip karo
            # kyunki "solid" trade ke liye entry/stoploss/target zaroori hai
            if trade_levels is None:
                continue

            # High risk-reward filter - jo user ne maanga hai
            if trade_levels["risk_reward_ratio"] < MIN_RISK_REWARD_RATIO:
                continue

            signals.append({
                "stock": stock["company"].title(),
                "symbol": stock["symbol"],
                "direction": sentiment["direction"],
                "confidence": sentiment["confidence"],
                "category": sentiment["category"],
                "reason": ", ".join(sentiment["matched_keywords"][:3]),
                "news_title": news["title"],
                "news_link": news["link"],
                "source": news["source"],
                "entry": trade_levels["entry"],
                "stoploss": trade_levels["stoploss"],
                "target1": trade_levels["target1"],
                "target2": trade_levels["target2"],
                "risk_reward_ratio": trade_levels["risk_reward_ratio"],
            })

        sent_cache.add(news["id"])

    _save_sent_cache(sent_cache)
    return signals


if __name__ == "__main__":
    for s in generate_signals():
        print(s)
