# trade_manager.py

import json
from datetime import datetime

OPEN_TRADES_FILE = "open_trades.json"

def add_open_trade(symbol, entry_price, stop_loss, take_profit):
    try:
        trade = {
            "symbol": symbol,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        try:
            with open(OPEN_TRADES_FILE, "r", encoding="utf-8") as f:
                trades = json.load(f)
        except:
            trades = []

        trades = [t for t in trades if t["symbol"] != symbol]
        trades.append(trade)

        with open(OPEN_TRADES_FILE, "w", encoding="utf-8") as f:
            json.dump(trades, f, indent=4)

    except Exception as e:
        print(f"שגיאה בהוספת עסקה: {e}")
