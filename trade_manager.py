from utils import send_discord_message, save_to_excel
from config import DISCORD_PUBLIC_WEBHOOK
from datetime import datetime

trade_management_log = []

def manage_trades(open_trades):
    for trade in open_trades:
        symbol = trade.get("symbol")
        current_price = trade.get("current_price")
        entry_price = trade.get("entry_price")
        stop_loss = trade.get("stop_loss")
        take_profit = trade.get("take_profit")

        if not all([symbol, current_price, entry_price, stop_loss, take_profit]):
            continue  # דילוג אם חסרים נתונים

        # תנאי לניהול עסקה: המחיר התקדם ב־3% מהרמה ההתחלתית
        if current_price >= entry_price * 1.03:
            new_stop = round(entry_price * 1.01, 2)
            message = (
                f"ניהול עסקה ({symbol}):\n"
                f"המחיר התקדם מעל 3%, הבוט מעדכן סטופ לוס ל־{new_stop}$\n"
                f"טייק פרופיט נשאר על {take_profit}$"
            )
            send_discord_message(DISCORD_PUBLIC_WEBHOOK, message, message_type="management")
            log_trade_action(symbol, stop_loss, new_stop, take_profit, take_profit)


def log_trade_action(symbol, old_stop, new_stop, old_take, new_take):
    trade_management_log.append({
        "symbol": symbol,
        "old_stop_loss": old_stop,
        "new_stop_loss": new_stop,
        "old_take_profit": old_take,
        "new_take_profit": new_take,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    save_to_excel(trade_management_log, "trade_management_log.xlsx")
