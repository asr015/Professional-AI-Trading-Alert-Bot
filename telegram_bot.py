"""
telegram_bot.py
Signal ko sundar formatted message me Telegram pe bhejta hai.
"""
from telegram import Bot
from telegram.constants import ParseMode
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

bot = Bot(token=TELEGRAM_BOT_TOKEN)


CATEGORY_LABELS = {
    "RESULTS": "馃搳 Quarterly Results Impact",
    "SMART_MONEY": "馃悑 Smart Money (FII/DII/Bulk-Block Deal)",
    "ELECTION_MACRO": "馃彌锔� Election / Macro / RBI Policy",
    "CORPORATE_ACTION": "馃 Corporate Action (M&A/Order/Upgrade)",
    "REGULATORY_RISK": "鈿栵笍 Regulatory / Legal Risk",
    "OTHER": "馃摪 General News",
}


def format_signal_message(signal: dict) -> str:
    emoji = "馃煝" if signal["direction"] == "BUY" else "馃敶"
    category_label = CATEGORY_LABELS.get(signal.get("category", "OTHER"), "馃摪 General News")

    return (
        f"{emoji} <b>{signal['direction']} SIGNAL 鈥� {signal['symbol']}</b> {emoji}\n"
        f"鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹乗n"
        f"馃搱 <b>Stock:</b> {signal['stock']} ({signal['symbol']})\n"
        f"馃彿锔� <b>Category:</b> {category_label}\n"
        f"馃幆 <b>News Confidence:</b> {signal['confidence']}/100\n\n"
        f"馃挵 <b>TRADE PLAN</b>\n"
        f"   Entry: 鈧箋signal['entry']}\n"
        f"   馃洃 Stoploss: 鈧箋signal['stoploss']}\n"
        f"   馃幆 Target 1: 鈧箋signal['target1']}\n"
        f"   馃幆 Target 2: 鈧箋signal['target2']}\n"
        f"   鈿栵笍 Risk:Reward: 1:{signal['risk_reward_ratio']}\n\n"
        f"馃摪 <b>Reason:</b> {signal['reason']}\n"
        f"馃敆 <b>News:</b> {signal['news_title']}\n"
        f"馃摗 <b>Source:</b> {signal['source']}\n"
        f"馃憠 <a href='{signal['news_link']}'>Full news padho</a>\n"
        f"鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹乗n"
        f"鈿狅笍 <i>Automated news-based signal hai, financial advice nahi. "
        f"Stoploss/target ATR (volatility) se calculate hue hain, guarantee nahi. "
        f"Apna risk khud manage karo, 1-2% se zyada capital ek trade me mat lagana.</i>"
    )


async def send_signal(signal: dict):
    message = format_signal_message(signal)
    await bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text=message,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=False,
    )


async def send_plain_message(text: str):
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)
