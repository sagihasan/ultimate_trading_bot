# scheduler.py

import time
import threading
from macro_monitor import check_upcoming_macro_events
from gap_detector import check_gap_signals
from trade_management import manage_open_trades
from daily_summary import send_nightly_summary
from datetime import datetime
import pytz

def run_scheduled_tasks():
    while True:
        now = datetime.now(pytz.timezone("Asia/Jerusalem"))
        current_time = now.strftime("%H:%M")

        # כל שעה עגולה – בדיקת אירועי מאקרו מתקרבים
        if now.minute == 0:
            check_upcoming_macro_events()

        # 22:30 רגיל / 21:30 פערי שעון / 19:30 חצי יום – ניהול עסקאות
        if current_time in ["22:30", "21:30", "19:30"]:
            manage_open_trades()

        # סיכום יומי – כל לילה ב־02:00
        if current_time == "02:00":
            send_nightly_summary()

        # בדיקת גאפ – כל יום ב־23:15
        if current_time == "23:15":
            check_gap_signals()

        time.sleep(60)  # המתן דקה לפני הבדיקה הבאה

# כדי להפעיל את הסקדולר ברקע
def start_scheduler():
    scheduler_thread = threading.Thread(target=run_scheduled_tasks)
    scheduler_thread.daemon = True
    scheduler_thread.start()
