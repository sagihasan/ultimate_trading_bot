# trade_management.py

import json
from datetime import datetime
from pathlib import Path

TRADE_LOG_PATH = Path("trade_log.json")
OPEN_TRADES_PATH = Path("open_trades.json")

def load_open_trades():
    if OPEN_TRADES_PATH.exists():
        with open(OPEN_TRADES_PATH, "r") as f:
            return json.load(f)
    return []

def save_open_trades(trades):
    with open(OPEN_TRADES_PATH, "w") as f:
        json.dump(trades, f, indent=2)

def log_trade_result(trade_result):
    if TRADE_LOG_PATH.exists():
        with open(TRADE_LOG_PATH, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(trade_result)

    with open(TRADE_LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)

def create_trade_entry(symbol, direction, entry_price, stop_loss, take_profit, reason, zone, market_rating):
    return {
        "תאריך": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "מניה": symbol,
        "סוג עסקה": direction,
        "מחיר כניסה": entry_price,
        "סטופ לוס": stop_loss,
        "טייק פרופיט": take_profit,
        "תוצאה": "",
        "(%) תשואה": "",
        "אזור מיוחד": zone,
        "תחזית שוק": market_rating,
        "סיבה": reason
    }
