# scheduler.py

import time
import threading
from macro_monitor import check_upcoming_macro_events
from gap_detector import check_gap_signals
from trade_management import manage_open_trades
from daily_summary import send_nightly_summary
from screener import run_screener
from datetime import datetime
import pytz

def run_scheduled_tasks():
    while True:
        now = datetime.now(pytz.timezone("Asia/Jerusalem"))
        current_time = now.strftime("%H:%M")

        # כל שעה עגולה – בדיקת מאקרו
        if now.minute == 0:
            check_upcoming_macro_events()

        # ניהול עסקאות – לפי סוג היום
        if current_time in ["22:30", "21:30", "19:30"]:
            manage_open_trades()

        # סיכום יומי – ב־02:00
        if current_time == "02:00":
            send_nightly_summary()

        # בדיקת גאפ – ב־23:15
        if current_time == "23:15":
            check_gap_signals()

        # סקרינר יומי – לפני פתיחת המסחר
        if current_time == "15:45":
            run_screener()

        time.sleep(60)

def start_scheduler():
    scheduler_thread = threading.Thread(target=run_scheduled_tasks)
    scheduler_thread.daemon = True
    scheduler_thread.start()
