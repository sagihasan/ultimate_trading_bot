# main.py

from fundamentals import analyze_fundamentals
from technicals import analyze_technicals
from macro import get_macro_summary, is_market_bullish
from discord_manager import send_discord_message, create_embed
from config import *
from stock_list import STOCK_LIST
import yfinance as yf
import datetime

def run_bot():
    now = datetime.datetime.now()
    signal = {}

    # ניתוח מאקרו
    macro_summary = get_macro_summary()
    market_bullish = is_market_bullish(macro_summary)
    signal["macro_summary"] = macro_summary
    signal["market_bullish"] = market_bullish

    selected_stock = None
    selected_score = -1

    for symbol in STOCK_LIST:
        try:
            df = yf.download(symbol, period="6mo", interval="1d")
            if df is None or df.empty or len(df) < 60:
                continue

            fundamentals = analyze_fundamentals(symbol)
            technicals = analyze_technicals(df)

            score = 0
            if fundamentals.get("strong"):
                score += 2
            if technicals.get("ema_cross_up"):
                score += 1
            if technicals.get("trend") == "bullish":
                score += 1
            if technicals.get("zones", {}).get("in_golden_zone"):
                score += 1

            if score > selected_score:
                selected_score = score
                selected_stock = {
                    "symbol": symbol,
                    "fundamentals": fundamentals,
                    "technicals": technicals,
                    "score": score
                }

        except Exception as e:
            print(f"שגיאה בניתוח {symbol}: {e}")

    if selected_stock:
        message = f"**איתות יומי - {selected_stock['symbol']}**\n"
        message += f"תוצאה כוללת: {selected_stock['score']}/5\n"
        message += f"מגמת שוק: {'חיובית' if market_bullish else 'שלילית'}\n"
        message += f"ניתוח פונדמנטלי: {'חזק' if selected_stock['fundamentals'].get('strong') else 'חלש'}\n"
        message += f"ניתוח טכני: {selected_stock['technicals']['trend']}\n"
        message += f"בולינגר תחתון: {round(selected_stock['technicals']['bb_lower'], 2)}\n"
        message += f"EMA9: {round(selected_stock['technicals']['ema_9'], 2)} | EMA20: {round(selected_stock['technicals']['ema_20'], 2)}\n"

        if selected_stock['technicals']["zones"]["in_golden_zone"]:
            message += "המניה נמצאת ב־Golden Zone\n"

        send_discord_message(message)

    else:
        send_discord_message("לא נמצא איתות מתאים היום.")
