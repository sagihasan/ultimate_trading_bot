# scheduler.py – ניהול עסקאות ודוחות

import time
from datetime import datetime
from reporting import generate_weekly_report, generate_monthly_report
from trade_manager import manage_trades
from utils import load_trade_data, load_open_trades, send_discord_message
from config import DISCORD_PRIVATE_WEBHOOK


def run_scheduler():
    while True:
        now = datetime.now()
        day = now.weekday()
        hour = now.hour
        minute = now.minute

        trades = load_trade_data()
        returns = [t.get("cumulative_return", 0) for t in trades]
        open_trades = load_open_trades()

        # דוח שבועי – שבת (יום 5) ב־12:00
        if day == 5 and hour == 12 and minute == 0:
            generate_weekly_report(trades, returns)

        # דוח חודשי – כל 1 לחודש ב־12:00
        if now.day == 1 and hour == 12 and minute == 0:
            generate_monthly_report(trades, returns)

        # ניהול עסקאות – כל חצי שעה (10:00–22:00) אם יש עסקאות פתוחות
        if 10 <= hour <= 22 and minute in [0, 30] and open_trades:
            manage_trades(open_trades)

        # שליחת עדכון יומי כל יום בשעה 02:00 בלילה
        if hour == 2 and minute == 0 and day in [0, 1, 2, 3, 4]:  # שני עד שישי
            try:
                send_discord_message(DISCORD_PRIVATE_WEBHOOK, "הבוט שלח עדכון יומי לערוץ הציבורי", message_type="log")
            except:
                pass

        time.sleep(60)


if __name__ == "__main__":
    run_scheduler()
