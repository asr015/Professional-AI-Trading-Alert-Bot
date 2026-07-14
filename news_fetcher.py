"""
news_fetcher.py
Free, real-time news fetching - RSS feeds se. Koi API key nahi chahiye.
"""
import feedparser
import hashlib
import time
from config import GENERAL_MARKET_RSS_FEEDS


def _make_news_id(title: str, link: str) -> str:
    """Har news article ka unique ID (duplicate detect karne ke liye)"""
    return hashlib.md5(f"{title}{link}".encode("utf-8")).hexdigest()


def fetch_latest_news(max_age_minutes: int = 30) -> list:
    """
    Saare RSS feeds se latest news uthata hai.
    Returns: list of dicts -> {id, title, summary, link, published, source}
    """
    all_news = []
    cutoff_time = time.time() - (max_age_minutes * 60)

    for feed_url in GENERAL_MARKET_RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            source_name = feed.feed.get("title", feed_url)

            for entry in feed.entries:
                title = entry.get("title", "")
                summary = entry.get("summary", "") or entry.get("description", "")
                link = entry.get("link", "")

                # Published time nikaalna (agar available hai)
                published_ts = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published_ts = time.mktime(entry.published_parsed)

                # Purani news skip karo (max_age_minutes se zyada purani)
                if published_ts and published_ts < cutoff_time:
                    continue

                all_news.append({
                    "id": _make_news_id(title, link),
                    "title": title,
                    "summary": summary,
                    "link": link,
                    "published": published_ts or time.time(),
                    "source": source_name,
                })
        except Exception as e:
            print(f"[news_fetcher] Feed fetch fail ho gaya {feed_url}: {e}")
            continue

    # Sabse naya news pehle
    all_news.sort(key=lambda x: x["published"], reverse=True)
    return all_news


if __name__ == "__main__":
    # Quick test run
    news = fetch_latest_news()
    print(f"Total {len(news)} news items mile")
    for n in news[:5]:
        print(f"- {n['title']} ({n['source']})")
