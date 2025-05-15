import json
import pandas as pd
import os
from datetime import datetime
from discord_manager import send_discord_message

TRADE_MANAGEMENT_LOG = "data/trade_management_log.xlsx"
OPEN_TRADES_FILE = "open_trades.json"

def load_open_trades():
    if not os.path.exists(OPEN_TRADES_FILE):
        return {}
    with open(OPEN_TRADES_FILE, 'r') as f:
        return json.load(f)

def save_management_recommendation(ticker, old_sl, new_sl, old_tp, new_tp, note):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = {
        "תאריך": timestamp,
        "מניה": ticker,
        "סטופ קודם": old_sl,
        "סטופ חדש": new_sl,
        "טייק קודם": old_tp,
        "טייק חדש": new_tp,
        "תוצאה צפויה": note
    }

    if os.path.exists(TRADE_MANAGEMENT_LOG):
        df = pd.read_excel(TRADE_MANAGEMENT_LOG)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_excel(TRADE_MANAGEMENT_LOG, index=False)

def manage_open_trades():
    trades = load_open_trades()
    for symbol, info in trades.items():
        entry = info.get("entry_price")
        current = info.get("current_price")
        stop = info.get("stop_loss")
        take = info.get("take_profit")
        direction = info.get("direction", "long")

        # כללים פשוטים להדגמה (אפשר להחליף באלגוריתם חכם יותר)
        new_stop = stop
        new_take = take
        recommendation = ""

        if direction == "long":
            if current >= entry * 1.03:
                new_stop = entry * 1.01
                new_take = entry * 1.06
                recommendation = "עדכון סטופ + טייק"
            elif current < stop * 1.01:
                recommendation = "חולשה – שקול יציאה"

        elif direction == "short":
            if current <= entry * 0.97:
                new_stop = entry * 0.99
                new_take = entry * 0.94
                recommendation = "עדכון סטופ + טייק"
            elif current > stop * 0.99:
                recommendation = "חולשה – שקול יציאה"

        if recommendation:
            msg = f"""**המלצת ניהול עסקה – {symbol}**
סטופ קודם: {round(stop, 2)} | חדש: {round(new_stop, 2)}
טייק קודם: {round(take, 2)} | חדש: {round(new_take, 2)}
{recommendation}"""
            send_discord_message(msg)
            save_management_recommendation(symbol, stop, new_stop, take, new_take, recommendation)
