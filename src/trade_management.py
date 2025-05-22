# trade_management.py

import json
from datetime import datetime
from pathlib import Path
import pandas as pd
from utils import get_current_time
from discord_manager import send_trade_update_message

TRADE_LOG_PATH = Path("data/trade_log.json")
OPEN_TRADES_PATH = Path("data/open_trades.json")
TRADE_MANAGEMENT_LOG = Path("data/trade_management_log.xlsx")

def create_trade_entry(symbol, direction, entry_price, stop_loss, take_profit, zone, market_rating, reason):
    return {
        "תאריך": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "מניה": symbol,
        "סוג עסקה": direction,
        "מחיר כניסה": entry_price,
        "סטופ לוס": stop_loss,
        "טייק פרופיט": take_profit,
        "אזור": zone,
        "הערכת שוק": market_rating,
        "סיבה": reason
    }

def log_trade_result(trade_result):
    if TRADE_LOG_PATH.exists():
        with open(TRADE_LOG_PATH, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(trade_result)

    with open(TRADE_LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)

def load_open_trades():
    if OPEN_TRADES_PATH.exists():
        with open(OPEN_TRADES_PATH, "r") as f:
            return json.load(f)
    return []

def save_open_trades(trades):
    with open(OPEN_TRADES_PATH, "w") as f:
        json.dump(trades, f, indent=2)

def manage_open_trades():
    try:
        if not OPEN_TRADES_PATH.exists():
            return

        with open(OPEN_TRADES_PATH, "r") as f:
            trades = json.load(f)

        updated_logs = []
        for trade in trades:
            entry_price = float(trade.get("מחיר כניסה", 0))
            stop_loss = float(trade.get("סטופ לוס", 0))
            take_profit = float(trade.get("טייק פרופיט", 0))
            symbol = trade.get("מניה")
            direction = trade.get("סוג עסקה")
            current_price = get_current_price(symbol)  # ודא שהפונקציה קיימת ב-price_utils

            if direction == "לונג":
                profit_pct = ((current_price - entry_price) / entry_price) * 100
            else:  # שורט
                profit_pct = ((entry_price - current_price) / entry_price) * 100

            new_stop = round(entry_price, 2)
            new_take = round(take_profit, 2)
            recommendation = ""

            if profit_pct >= 3:
                new_stop = round(entry_price * 1.01, 2) if direction == "לונג" else round(entry_price * 0.99, 2)
                recommendation = "המלצה: להזיז סטופ לוס לרווח"
            elif profit_pct <= -2:
                recommendation = "המלצה: שקול לסגור את העסקה – הפסד חורג"

            message = f"""עדכון עסקה:
מניה: {symbol}
סוג עסקה: {direction}
מחיר נוכחי: {current_price}
רווח/הפסד נוכחי: {round(profit_pct, 2)}%
{recommendation}"""

            send_trade_update_message(message)
            send_message_with_delay(send_public_message, message, delay=RATE_LIMIT_SECONDS)

            updated_logs.append({
                "תאריך": get_current_time().strftime("%Y-%m-%d %H:%M"),
                "מניה": symbol,
                "עסקה": direction,
                "מחיר נוכחי": current_price,
                "סטופ קודם": stop_loss,
                "סטופ חדש": new_stop,
                "טייק קודם": take_profit,
                "טייק חדש": new_take,
                "תוצאה צפויה": f"{round(profit_pct, 2)}%"
            })

        # שמירת לוג ניהול עסקאות
        df = pd.DataFrame(updated_logs)
        if TRADE_MANAGEMENT_LOG.exists():
            existing = pd.read_excel(TRADE_MANAGEMENT_LOG)
            df = pd.concat([existing, df], ignore_index=True)
        df.to_excel(TRADE_MANAGEMENT_LOG, index=False)

    except Exception as e:
        print(f"שגיאה בניהול עסקאות פתוחות: {e}")
