# main.py

from fundamentals import analyze_fundamentals
from technicals import analyze_technicals
from macro import get_macro_summary, is_market_bullish
from discord_manager import send_public_message, send_error_message
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
    selected_score = 0

    for symbol in STOCK_LIST:
        try:
            stock = yf.Ticker(symbol)
            df = stock.history(period="6mo")
            if df.empty:
                continue

            fundamentals = analyze_fundamentals(symbol)
            technicals = analyze_technicals(df)

            score = 0
            if market_bullish and technicals['trend'] == "עלייה":
                score += 1
            if fundamentals['strong']:
                score += 1
            if technicals['bb'] > 0.5:
                score += 1
            if technicals['ema_9'] > 0.5:
                score += 1
            if technicals['zones']['in_golden_zone']:
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
            send_error_message(f"שגיאה בניתוח {symbol}:\n{e}")

    if selected_stock:
        message = f"**איתות יומי – {selected_stock['symbol']}**\n"
        message += f"תרחיש כולל: {'חיובי' if market_bullish else 'שלילי'}\n"
        message += f"ציון כולל: {selected_stock['score']}/5\n"
        message += f"מגמת שוק: {selected_stock['technicals']['trend']}\n"
        message += f"מדד בולינגר: {round(selected_stock['technicals']['bb'], 2)}\n"
        message += f"EMA9: {round(selected_stock['technicals']['ema_9'], 2)}\n"

        if selected_stock['technicals']['zones']['in_golden_zone']:
            message += "המניה נמצאת ב־Golden Zone\n"

        send_public_message(message)

    else:
        send_public_message("לא נמצא איתות מתאים היום.")
