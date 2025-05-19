# main.py

from fundamentals import analyze_fundamentals
from technicals import analyze_technicals
from macro import get_macro_summary, is_market_bullish, detect_upcoming_crisis, detect_gap_warning_from_macro
from discord_manager import send_discord_message, create_signal_message
from config import *
from stock_list import STOCK_LIST
import yfinance as yf
import datetime

def run_bot():
    today = datetime.datetime.now()
    signal_sent = False

    # ניתוח מאקרו כולל והשפעה
    macro_summary = get_macro_summary()
    market_bullish = is_market_bullish(macro_summary)

    for ticker in STOCK_LIST:
        df = yf.download(ticker, period="6mo")

        if df is None or df.empty or len(df) < 60:
            continue

        fundamentals = analyze_fundamentals(ticker)
        technicals = analyze_technicals(df)

        # תנאי חובה פונדומנטליים
        if not fundamentals["passes"]:
            continue

        # תנאי טכני - דרושים לפחות 4 איתותים מחזקים
        strong_signals = technicals.get("strong_signals", 0)
        if strong_signals < 4:
            continue

        # הכנת איתות מלא
        signal = {
            "ticker": ticker,
            "direction": technicals.get("trend", "לא זמין"),
            "order_type": "Market",
            "entry_price": round(df["Close"].iloc[-1], 2),
            "stop_loss": round(df["Close"].iloc[-1] * 0.97, 2),
            "take_profit": round(df["Close"].iloc[-1] * 1.05, 2),
            "trend_sentiment": technicals.get("trend", "לא זמין"),
            "zones": technicals.get("zones", {}),
            "risk_pct": 3,
            "risk_dollars": 100,
            "reward_pct": 5,
            "reward_dollars": 170,
            "ai_score": technicals.get("ai_score", 0),
            "confidence_score": technicals.get("confidence", 0),
            "bot_decision": "המלצה להיכנס לעסקה",
            "macro_summary": macro_summary,
            "market_bullish": market_bullish
        }

        message = create_signal_message(signal)
        send_discord_message(message)
        signal_sent = True
        break

    if not signal_sent:
        send_discord_message("לא נשלח איתות היום כי לא נמצאה מניה שעומדת בכל התנאים.")
