from utils import send_discord_message, save_to_excel
from config import DISCORD_PUBLIC_WEBHOOK
from datetime import datetime

trade_management_log = []


def manage_trades(open_trades):
    for trade in open_trades:
        symbol = trade["symbol"]
        current_price = trade["current_price"]
        entry_price = trade["entry_price"]
        stop_loss = trade["stop_loss"]
        take_profit = trade["take_profit"]

        # דוגמה לניהול עסקה: עדכון סטופ לוס כשהרווח עובר 3%
        if current_price >= entry_price * 1.03:
            new_stop = round(entry_price * 1.01, 2)
            message = (
                f"ניהול עסקה ({symbol}):\n"
                f"המחיר התקדם מעל 3%, הבוט מעדכן סטופ לוס ל-{new_stop}$\n"
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
