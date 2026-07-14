"""
check_signals.py
Yeh main.py se alag hai - yeh EK BAAR news check karta hai, signals bhejta
hai, aur exit ho jaata hai. GitHub Actions ke liye bana hai (jo har run
me fresh process start karta hai, continuous server nahi chalata).

Chalane ka tarika:
    python check_signals.py
"""
import asyncio
import logging

from signal_generator import generate_signals
from telegram_bot import send_signal

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("check-signals")


async def run_check():
    logger.info("News check ho raha hai (GitHub Actions run)...")
    signals = generate_signals()

    if not signals:
        logger.info("Koi high-probability signal nahi mila is baar.")
        return

    for signal in signals:
        logger.info(
            f"Signal mila: {signal['symbol']} {signal['direction']} "
            f"(confidence: {signal['confidence']}, R:R 1:{signal['risk_reward_ratio']})"
        )
        await send_signal(signal)

    logger.info(f"Total {len(signals)} signal(s) bheja gaya.")


if __name__ == "__main__":
    asyncio.run(run_check())
