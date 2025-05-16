# trade_management.py

import json
from discord_manager import send_discord_message
from datetime import datetime

OPEN_TRADES_FILE = "open_trades.json"
LOG_FILE = "data/trade_management_log.xlsx"

def manage_open_trades():
    try:
        with open(OPEN_TRADES_FILE, "r", encoding="utf-8") as f:
            trades = json.load(f)

        updated_trades = []

        for trade in trades:
            symbol = trade["symbol"]
            current_price = trade.get("current_price", trade["entry_price"] * 1.03)
            stop_loss = trade["stop_loss"]
            take_profit = trade["take_profit"]

            message = f"""**ניהול עסקה – {symbol}**
מחיר נוכחי: {current_price}
סטופ קודם: {stop_loss}
טייק קודם: {take_profit}
"""

            # אם יש רווח נאה – קדם סטופ
            if current_price > take_profit * 0.95:
                new_stop = round(current_price * 0.98, 2)
                message += f"\nהבוט קובע: להזיז סטופ ל־{new_stop} ולשמור יעד רווח."
                trade["stop_loss"] = new_stop
                updated_trades.append(trade)

            elif current_price < stop_loss * 1.01:
                message += f"\nהבוט קובע: לצאת מהעסקה עכשיו – מגמה נשברת."
                continue  # לא נוסיף לרשימה

            else:
                message += f"\nאין שינוי. הבוט עוקב."

                updated_trades.append(trade)

            send_discord_message(message)

        # שמירה חזרה
        with open(OPEN_TRADES_FILE, "w", encoding="utf-8") as f:
            json.dump(updated_trades, f, indent=4)

    except Exception as e:
        send_discord_message(f"שגיאה בניהול עסקאות:\n{e}")
