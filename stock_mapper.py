"""
stock_mapper.py
News ke text me se company ka naam dhundh kar NSE symbol return karta hai.
Fuzzy matching use karta hai taaki "Reliance Ind." jaisi variations bhi pakdi jaayein.
"""
import json
from difflib import SequenceMatcher
from config import STOCK_SYMBOLS_FILE


def _similarity(a: str, b: str) -> float:
    """0-100 scale similarity score, difflib ka use karke (stdlib, no extra install)"""
    return SequenceMatcher(None, a, b).ratio() * 100

with open(STOCK_SYMBOLS_FILE, "r", encoding="utf-8") as f:
    _raw_map = json.load(f)

# _comment jaisi placeholder keys hata do
COMPANY_TO_SYMBOL = {k.lower(): v for k, v in _raw_map.items() if not k.startswith("_")}
COMPANY_NAMES = list(COMPANY_TO_SYMBOL.keys())


def find_stocks_in_text(text: str, min_score: int = 88) -> list:
    """
    Text me se saari matching companies dhundhta hai.
    Returns: list of dicts -> {company, symbol, match_score}
    """
    text_lower = text.lower()
    found = []
    seen_symbols = set()

    # Step 1: Exact substring match (fast aur reliable)
    for company_name, symbol in COMPANY_TO_SYMBOL.items():
        if company_name in text_lower and symbol not in seen_symbols:
            found.append({"company": company_name, "symbol": symbol, "match_score": 100})
            seen_symbols.add(symbol)

    # Step 2: Agar exact match kam mila, fuzzy match try karo (typo/variation ke liye)
    if not found:
        words = text_lower.split()
        # 2-3 word combinations bana kar company names se compare karo
        candidates = set(words)
        for i in range(len(words) - 1):
            candidates.add(f"{words[i]} {words[i+1]}")

        for candidate in candidates:
            for company_name, symbol in COMPANY_TO_SYMBOL.items():
                if symbol in seen_symbols:
                    continue
                score = _similarity(candidate, company_name)
                if score >= min_score:
                    found.append({"company": company_name, "symbol": symbol, "match_score": score})
                    seen_symbols.add(symbol)

    return found


if __name__ == "__main__":
    test_text = "Reliance Industries posts record profit, beats estimates in Q3"
    print(find_stocks_in_text(test_text))
