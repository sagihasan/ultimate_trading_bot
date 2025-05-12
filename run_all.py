# run_all.py – הפעלת הבוט הראשי ודוחות במקביל

import threading
import time
from main import main as run_main
from reporting import generate_weekly_report, generate_monthly_report
from trade_manager import manage_trades
from utils import load_trade_data, load_open_trades
from datetime import datetime

def run_scheduler():
    while True:
        now = datetime.now()
        day = now.weekday()  # יום בשבוע (0=שני, 6=ראשון)
        hour = now.hour
        minute = now.minute

        trades = load_trade_data()
        returns = [t.get("cumulative_return", 0) for t in trades]
        open_trades = load_open_trades()

        # דוח שבועי – שבת ב־12:00
        if day == 5 and hour == 12 and minute == 0:
            generate_weekly_report(trades, returns)

        # דוח חודשי – 1 לחודש ב־12:00
        if now.day == 1 and hour == 12 and minute == 0:
            generate_monthly_report(trades, returns)

        # ניהול עסקאות – כל חצי שעה בין 10:00–23:00 אם יש עסקאות פתוחות
        if hour in range(10, 23) and minute in [0, 30] and open_trades:
            manage_trades(open_trades)

        time.sleep(60)  # כל דקה

if __name__ == "__main__":
    # חוט ראשי – בוט יומי (איתותים)
    main_thread = threading.Thread(target=run_main)
    main_thread.start()

    # חוט שני – ניהול עסקאות ודוחות
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    # שמירה על תהליכים חיים
    while True:
        time.sleep(60)
