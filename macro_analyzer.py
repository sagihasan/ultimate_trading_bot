# macro_analyzer.py

from macro import analyze_macro_conditions
from fundamentals import get_fundamentals

def evaluate_macro_and_fundamentals(symbol):
    fundamentals = get_fundamentals(symbol)
    macro = analyze_macro_conditions()

    summary = {
        "symbol": symbol,
        "macro_sentiment": macro["macro_sentiment"],
        "macro_note": macro["note"],
        "growth_type": fundamentals.get("growth_type", "ניטרלית"),
        "sentiment": fundamentals.get("sentiment", "ניטרלי"),
        "buffett_zone": fundamentals.get("in_buffett_zone", False),
        "pe_ratio": fundamentals.get("pe_ratio", 0)
    }

    return summary
