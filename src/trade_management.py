import json
import os
from datetime import datetime
from discord_manager import send_trade_update_message
from utils import get_current_time

TRADE_LOG_PATH = "data/open_trades.json"

def load_open_trades():
    if os.path.exists(TRADE_LOG_PATH):
        with open(TRADE_LOG_PATH, "r") as f:
            return json.load(f)
    return []

def save_open_trades(trades):
    with open(TRADE_LOG_PATH, "w") as f:
        json.dump(trades, f, indent=2)

def manage_open_trades():
    now = get_current_time()
    trades = load_open_trades()
    updated_trades = []

    for trade in trades:
        entry_price = trade["entry_price"]
        stop_loss = trade["stop_loss"]
        take_profit = trade["take_profit"]
        current_price = trade.get("current_price", entry_price)  # נניח אם אין עדכון

        message = ""
        if current_price <= stop_loss:
            message = f"העסקה על {trade['ticker']} הגיעה לסטופ לוס ({stop_loss}) – מומלץ לצאת."
        elif current_price >= take_profit:
            message = f"העסקה על {trade['ticker']} הגיעה לטייק פרופיט ({take_profit}) – מומלץ לסגור רווח."
        else:
            updated_trades.append(trade)  # שמור רק את אלו שלא הסתיימו

        if message:
            send_trade_update_message(message)

    save_open_trades(updated_trades)
