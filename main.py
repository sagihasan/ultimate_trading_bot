import os
import time
from datetime import datetime
from config import *
from discord_manager import send_discord_message, send_error_message
from fundamentals import get_fundamentals
from technicals import analyze_technicals
from macro_analyzer import analyze_macro_conditions
from risk_management import calculate_stop_loss, calculate_take_profit
from trade_manager import load_open_trades, save_trade, close_trade
from trade_management import manage_open_trades
from log_manager import log_error
from zones import check_zones
from screener import get_stock_list

def is_market_open():
    now = datetime.now()
    return now.weekday() < 5 and MARKET_OPEN_HOUR <= now.hour < MARKET_CLOSE_HOUR

def analyze_stock(symbol):
    try:
        fundamentals = get_fundamentals(symbol)
        if not fundamentals:
            return None

        technicals = analyze_technicals(symbol)
        macro = analyze_macro_conditions()
        zones_info = check_zones(symbol)

        all_conditions = {
            "fundamentals": fundamentals,
            "technicals": technicals,
            "macro": macro,
            "zones": zones_info
        }

        # תנאי חובה: פונדומנטלי + 4 תנאים טכניים
        mandatory = fundamentals["growth_type"] != "צניחה" and fundamentals["market_cap"] > 1_000_000_000
        tech_conditions = sum([
            technicals.get("ma_crossover", False),
            technicals.get("rsi_ok", False),
            technicals.get("macd_ok", False),
            technicals.get("volume_ok", False),
            technicals.get("price_action_ok", False),
            zones_info.get("in_demand_zone", False)
        ])

        if mandatory and tech_conditions >= 4:
            return {
                "symbol": symbol,
                "entry_price": technicals.get("entry_price"),
                "stop_loss": calculate_stop_loss(technicals.get("entry_price"), "long"),
                "take_profit": calculate_take_profit(technicals.get("entry_price"), "long"),
                "direction": "long",
                "fundamentals": fundamentals,
                "macro": macro,
                "zones": zones_info
            }
        return None
    except Exception as e:
        log_error(f"שגיאה בניתוח מניה {symbol}: {e}")
        return None
def create_signal_message(data):
    f = data["fundamentals"]
    m = data["macro"]
    z = data["zones"]
    symbol = data["symbol"]
    entry = round(data["entry_price"], 2)
    sl = round(data["stop_loss"], 2)
    tp = round(data["take_profit"], 2)
    sentiment = f["sentiment"]
    growth = f["growth_type"]
    macro_note = m["note"]
    zone_status = "Yes" if z.get("in_demand_zone") else "No"

    # תוכל לשנות ידנית או לדחוף לדינמיקה בהמשך
    order_type = "Stop Limit"  # אפשר: Market, Limit, Stop, Stop Limit

    # ניסוח פקודה לפי סוג
    if order_type.lower() == "market":
        price_line = f"פקודת כניסה: **Market** – כניסה מיידית לפי המחיר הזמין בשוק."
    elif order_type.lower() in ["limit", "stop", "stop limit"]:
        price_line = f"פקודת כניסה: **{order_type}** במחיר: {entry}"
    else:
        price_line = f"פקודת כניסה: **{order_type}**"

    message = f"""**איתות קרבי – {symbol}**
{price_line}
סטופ לוס: {sl}
טייק פרופיט: {tp}
מחיר נוכחי: {entry}
סנטימנט: {sentiment}
צמיחה: {growth}
מאקרו: {macro_note}
אזור אסטרטגי: {zone_status}

**הוראה: להיכנס לעסקה. אין פשרות. הביצוע עכשיו.**
"""
    return message
    def run_trade_management():
    try:
        manage_open_trades()
    except Exception as e:
        log_error(f"שגיאה בניהול עסקאות פתוחות: {e}")

def fallback_signal_if_needed():
    try:
        now = datetime.now()
        if now.hour == 22 and now.minute >= 40:
            open_trades = load_open_trades()
            if not open_trades:
                send_discord_message("22:40 – לא נשלח איתות היום. הסיבה: אף מניה לא עמדה בכל התנאים הקרביים.")
    except Exception as e:
        log_error(f"שגיאה ב־fallback_signal_if_needed: {e}")

if __name__ == "__main__":
    print("הבוט התחיל לעבוד.")
    run_bot()
    run_trade_management()
    fallback_signal_if_needed()
