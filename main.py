"""
main.py
Bot ka entry point. Render (aur Railway) ke liye ek Flask "web service"
ke roop me chalta hai (health-check endpoint deta hai), aur background me
scheduler har X minute me news check karke Telegram signals bhejta hai.

Yeh design isliye hai taaki Render ke FREE tier pe deploy ho sake -
free tier pe sirf "web service" type chalta hai (background worker nahi),
aur UptimeRobot jaisi free service isse "/ping" pe hit karke 24x7 jagaye rakhti hai.

Chalane ka tarika (local):
    python main.py
"""
import asyncio
import logging
import threading
from datetime import datetime, timezone

from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler

from signal_generator import generate_signals
from telegram_bot import send_signal, send_plain_message
from config import POLL_INTERVAL_MINUTES, PORT

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("news-trading-bot")

app = Flask(__name__)

# Bot ki current status track karne ke liye (health endpoint pe dikhane ke liye)
bot_status = {
    "started_at": None,
    "last_check": None,
    "last_check_signals_found": 0,
    "total_signals_sent": 0,
}


def check_and_send_signals():
    """Yeh function scheduler har X minute me call karta hai (sync wrapper, async telegram call ke liye)"""
    logger.info("News check ho raha hai...")
    bot_status["last_check"] = datetime.now(timezone.utc).isoformat()
    try:
        signals = generate_signals()
        bot_status["last_check_signals_found"] = len(signals)

        if not signals:
            logger.info("Koi high-probability signal nahi mila is baar.")
            return

        for signal in signals:
            logger.info(
                f"Signal mila: {signal['symbol']} {signal['direction']} "
                f"(confidence: {signal['confidence']}, R:R 1:{signal['risk_reward_ratio']})"
            )
            asyncio.run(send_signal(signal))
            bot_status["total_signals_sent"] += 1
    except Exception as e:
        logger.error(f"Error signal generation me: {e}")


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_and_send_signals, "interval", minutes=POLL_INTERVAL_MINUTES)
    scheduler.start()
    logger.info(f"Scheduler start ho gaya - har {POLL_INTERVAL_MINUTES} minute me check karega")


@app.route("/")
@app.route("/ping")
def health_check():
    """
    UptimeRobot / cron-job.org isi endpoint ko har 5-10 minute me hit karega
    taaki Render ka free service sleep na ho (spin-down se bacha rahe).
    """
    return jsonify({
        "status": "alive",
        "bot": "news-trading-signals-bot",
        **bot_status,
    }), 200


def run_bot_background():
    """Bot ki background thread - startup message bhejta hai, scheduler start karta hai, ek turant check karta hai"""
    bot_status["started_at"] = datetime.now(timezone.utc).isoformat()
    try:
        asyncio.run(send_plain_message(
            "✅ News Trading Signal Bot start ho gaya hai (F&O stocks, "
            "results/election/smart-money news, live price target-stoploss ke saath)."
        ))
    except Exception as e:
        logger.error(f"Startup message bhejne me error: {e}")

    start_scheduler()
    check_and_send_signals()  # turant ek baar check kar lo


if __name__ == "__main__":
    # Background thread me bot chalao, Flask ko main thread me (Render ko web port chahiye)
    bot_thread = threading.Thread(target=run_bot_background, daemon=True)
    bot_thread.start()

    app.run(host="0.0.0.0", port=PORT)
