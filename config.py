"""
config.py
Saari settings yahan se load hoti hain. .env file me apne secrets daalo.
"""
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
POLL_INTERVAL_MINUTES = int(os.getenv("POLL_INTERVAL_MINUTES", "3"))
MIN_CONFIDENCE_SCORE = int(os.getenv("MIN_CONFIDENCE_SCORE", "75"))
MIN_RISK_REWARD_RATIO = float(os.getenv("MIN_RISK_REWARD_RATIO", "1.5"))
PORT = int(os.getenv("PORT", "8080"))

# Free real-time news sources - RSS feeds (no API key needed)
# Google News RSS is query-based, so hum stock names/keywords se dynamic query bana sakte hain
GOOGLE_NEWS_RSS_TEMPLATE = "https://news.google.com/rss/search?q={query}+when:1h&hl=en-IN&gl=IN&ceid=IN:en"

# General market RSS feeds (broad news, sab stocks cover karte hain)
GENERAL_MARKET_RSS_FEEDS = [
    "https://www.moneycontrol.com/rss/marketreports.xml",
    "https://www.moneycontrol.com/rss/latestnews.xml",
    "https://www.moneycontrol.com/rss/business.xml",
    "https://www.livemint.com/rss/markets",
    "https://www.business-standard.com/rss/markets-106.rss",
    "https://economictimes.indiatimes.com/markets/stocks/news/rssfeeds/2146842.cms",
]

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
STOCK_SYMBOLS_FILE = os.path.join(DATA_DIR, "stock_symbols.json")
SENTIMENT_LEXICON_FILE = os.path.join(DATA_DIR, "sentiment_lexicon.json")
KEYWORD_CATEGORIES_FILE = os.path.join(DATA_DIR, "keyword_categories.json")
CACHE_FILE = os.path.join(os.path.dirname(__file__), "sent_news_cache.json")

# Kitne purane sent-news IDs yaad rakhne hain (duplicate signal rokne ke liye)
MAX_CACHE_SIZE = 500
