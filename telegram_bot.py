"""
telegram_bot.py
Signal ko sundar formatted message me Telegram pe bhejta hai.
"""
from telegram import Bot
from telegram.constants import ParseMode
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

bot = Bot(token=TELEGRAM_BOT_TOKEN)


CATEGORY_LABELS = {
    "RESULTS": "ðŸ“Š Quarterly Results Impact",
    "SMART_MONEY": "ðŸ‹ Smart Money (FII/DII/Bulk-Block Deal)",
    "ELECTION_MACRO": "ðŸ›ï¸ Election / Macro / RBI Policy",
    "CORPORATE_ACTION": "ðŸ¤ Corporate Action (M&A/Order/Upgrade)",
    "REGULATORY_RISK": "âš–ï¸ Regulatory / Legal Risk",
    "OTHER": "ðŸ“° General News",
}


def format_signal_message(signal: dict) -> str:
    emoji = "ðŸŸ¢" if signal["direction"] == "BUY" else "ðŸ”´"
    category_label = CATEGORY_LABELS.get(signal.get("category", "OTHER"), "ðŸ“° General News")

    return (
        f"{emoji} <b>{signal['direction']} SIGNAL â€” {signal['symbol']}</b> {emoji}\n"
        f"â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”\n"
        f"ðŸ“ˆ <b>Stock:</b> {signal['stock']} ({signal['symbol']})\n"
        f"ðŸ·ï¸ <b>Category:</b> {category_label}\n"
        f"ðŸŽ¯ <b>News Confidence:</b> {signal['confidence']}/100\n\n"
        f"ðŸ’° <b>TRADE PLAN</b>\n"
        f"   Entry: â‚¹{signal['entry']}\n"
        f"   ðŸ›‘ Stoploss: â‚¹{signal['stoploss']}\n"
        f"   ðŸŽ¯ Target 1: â‚¹{signal['target1']}\n"
        f"   ðŸŽ¯ Target 2: â‚¹{signal['target2']}\n"
        f"   âš–ï¸ Risk:Reward: 1:{signal['risk_reward_ratio']}\n\n"
        f"ðŸ“° <b>Reason:</b> {signal['reason']}\n"
        f"ðŸ”— <b>News:</b> {signal['news_title']}\n"
        f"ðŸ“¡ <b>Source:</b> {signal['source']}\n"
        f"ðŸ‘‰ <a href='{signal['news_link']}'>Full news padho</a>\n"
        f"â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”\n"
        f"âš ï¸ <i>Automated news-based signal hai, financial advice nahi. "
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
