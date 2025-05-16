# main.py

from config import *
from fundamentals import get_fundamentals
from technicals import analyze_technicals
from macro import analyze_macro_conditions
from discord_manager import send_discord_message, send_error_message
from ml_model import predict_success_probability
from stock_list import STOCK_LIST
from risk_management import calculate_stop_loss, calculate_take_profit
from trade_management import manage_open_trades
from datetime import datetime
import pytz

def analyze_stock(symbol):
    try:
        fundamentals = get_fundamentals(symbol)
        technicals = analyze_technicals(symbol)
        macro = analyze_macro_conditions()

        if fundamentals["growth_type"] == "צניחה" or fundamentals["sentiment"] == "שלילי":
            return None

        features = {
            "rsi": technicals["rsi"],
            "macd": technicals["macd"],
            "volume": technicals["volume"],
            "ma_cross": technicals["ma_cross"],
            "in_demand_zone": technicals["in_demand_zone"],
            "in_buffett_zone": fundamentals["in_buffett_zone"],
            "sentiment_score": fundamentals["sentiment_score"],
            "weekly_trend": technicals["weekly_trend"],
            "daily_trend": technicals["daily_trend"]
        }

        score = predict_success_probability(features)
        if score >= 0.95:
            return {
                "symbol": symbol,
                "entry_price": technicals["entry_price"],
                "stop_loss": calculate_stop_loss(technicals["entry_price"]),
                "take_profit": calculate_take_profit(technicals["entry_price"]),
                "ai_score": round(score * 100),
                "growth_type": fundamentals["growth_type"],
                "sentiment": fundamentals["sentiment"],
                "macro_note": macro["note"]
            }

    except Exception as e:
        send_error_message(f"שגיאה בניתוח {symbol}:\n{e}")
        return None

def run_daily_signal():
    best_signal = None
    for symbol in STOCK_LIST:
        result = analyze_stock(symbol)
        if result:
            best_signal = result
            break

    if best_signal:
        message = f"""**איתות קרבי – {best_signal['symbol']}**
פקודת כניסה: **Market**
מחיר כניסה: {best_signal['entry_price']}
סטופ לוס: {best_signal['stop_loss']}
טייק פרופיט: {best_signal['take_profit']}

AI Score: {best_signal['ai_score']}/100  
סנטימנט: {best_signal['sentiment']}  
צמיחה: {best_signal['growth_type']}  
מאקרו: {best_signal['macro_note']}

**הבוט קובע: להיכנס לעסקה עכשיו.**
"""
        send_discord_message(message)
    else:
        send_discord_message("אין איתות היום – השוק מבולבל. אין כניסה. הבוט ממשיך לעקוב.")

def run_bot():
    try:
        # ניהול עסקאות – כל יום בזמן קבוע
        manage_open_trades()

        # איתות יומי – פעם אחת ביום
        current_time = datetime.now(pytz.timezone("Asia/Jerusalem")).strftime("%H:%M")
        if current_time == DAILY_SIGNAL_TIME:
            run_daily_signal()

    except Exception as e:
        send_error_message(f"שגיאת מערכת:\n{e}")

if __name__ == "__main__":
    run_bot())
