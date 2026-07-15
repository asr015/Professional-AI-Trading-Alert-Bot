"""
sentiment_analyzer.py
News text ko scan karke keywords ke basis pe bullish/bearish sentiment
aur ek confidence score (0-100) nikalta hai.

Logic simple aur transparent hai (koi black-box nahi):
- Har matched keyword ka apna weight hai (sentiment_lexicon.json me)
- Jitne zyada / strong keywords match honge, utna zyada confidence
- Bullish aur bearish dono keywords mil jaayein to "MIXED/SKIP" aata hai
  (kyunki wahan direction clear nahi hai - high probability ka matlab
  hai clarity, confusion nahi)
"""
import json
from config import SENTIMENT_LEXICON_FILE, KEYWORD_CATEGORIES_FILE

with open(SENTIMENT_LEXICON_FILE, "r", encoding="utf-8") as f:
    _lexicon = json.load(f)

with open(KEYWORD_CATEGORIES_FILE, "r", encoding="utf-8") as f:
    _categories_raw = json.load(f)

BULLISH_KEYWORDS = _lexicon["bullish"]
BEARISH_KEYWORDS = _lexicon["bearish"]

# keyword -> category, easy lookup ke liye reverse kar lete hain
KEYWORD_TO_CATEGORY = {}
for category, keywords in _categories_raw.items():
    for kw in keywords:
        KEYWORD_TO_CATEGORY[kw] = category


def _detect_category(matched_keywords: list) -> str:
    """Matched keywords me se sabse zyada common category return karta hai"""
    if not matched_keywords:
        return "OTHER"
    counts = {}
    for kw in matched_keywords:
        cat = KEYWORD_TO_CATEGORY.get(kw, "OTHER")
        counts[cat] = counts.get(cat, 0) + 1
    return max(counts, key=counts.get)


def analyze_sentiment(text: str) -> dict:
    """
    Returns: {
        "direction": "BUY" | "SELL" | "NEUTRAL",
        "confidence": int (0-100),
        "matched_keywords": [list of matched keyword strings]
    }
    """
    text_lower = text.lower()

    bull_score = 0
    bull_matches = []
    for keyword, weight in BULLISH_KEYWORDS.items():
        if keyword in text_lower:
            bull_score += weight
            bull_matches.append(keyword)

    bear_score = 0
    bear_matches = []
    for keyword, weight in BEARISH_KEYWORDS.items():
        if keyword in text_lower:
            bear_score += weight
            bear_matches.append(keyword)

    # Agar dono taraf strong signal hai, toh confusion hai - skip karo
    if bull_score > 0 and bear_score > 0:
        # Agar ek dusre se bahut zyada dominant hai (2x se zyada), tab bhi consider karo
        if bull_score >= bear_score * 2:
            direction = "BUY"
            confidence = min(100, bull_score)
            matched = bull_matches
        elif bear_score >= bull_score * 2:
            direction = "SELL"
            confidence = min(100, bear_score)
            matched = bear_matches
        else:
            return {"direction": "NEUTRAL", "confidence": 0, "matched_keywords": bull_matches + bear_matches, "category": "OTHER"}
    elif bull_score > 0:
        direction = "BUY"
        confidence = min(100, bull_score)
        matched = bull_matches
    elif bear_score > 0:
        direction = "SELL"
        confidence = min(100, bear_score)
        matched = bear_matches
    else:
        return {"direction": "NEUTRAL", "confidence": 0, "matched_keywords": [], "category": "OTHER"}

    category = _detect_category(matched)
    return {"direction": direction, "confidence": confidence, "matched_keywords": matched, "category": category}


if __name__ == "__main__":
    print(analyze_sentiment("Company X posts record profit, beats estimates, upgraded to buy"))
    print(analyze_sentiment("Company Y faces SEBI probe, CEO resigns amid fraud allegations"))
    print(analyze_sentiment("FIIs record buying seen, mutual fund buying stake increase in Company Z"))
    print(analyze_sentiment("RBI announces repo rate cut, exit poll favors stable government"))
