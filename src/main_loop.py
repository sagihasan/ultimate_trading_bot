from messaging import send_start_message, send_end_message
import os
from time_config import START_HOUR, START_MINUTE, END_HOUR, END_MINUTE, MACRO_EVENT_HOUR, MACRO_EVENT_MINUTE

send_message(os.getenv('DISCORD_PUBLIC_WEBHOOK_URL'), '✅ הבוט התחיל לפעול')

from datetime import datetime, timedelta
from pytz import timezone
import time

from src.main import run_bot


def send_final_signal():
    run_bot()


from scheduler_loop import (check_macro_alerts, send_start_message,
                            send_end_message, send_macro_event_summary_before,
                            send_macro_event_summary_after,
                            send_no_real_trading_alert)

from market_time_utils import get_market_close_hour, is_short_trading_day, is_no_real_trading

# הגדרות זמנים קבועים

# flags
sent_today_start = False
sent_today_end = False
sent_today_signal = False
sent_macro_before = False
sent_macro_after = False
sent_no_trading_alert = False
last_day = datetime.now().date()

# לולאת הבוט
while True:
    israel_tz = timezone('Asia/Jerusalem')
    now = datetime.now(israel_tz)
    today = now.date()
    current_hour = now.hour
    current_minute = now.minute

    # איפוס יומי
    if last_day != today:
        sent_today_start = False
        sent_today_end = False
        sent_today_signal = False
        sent_macro_before = False
        sent_macro_after = False
        sent_no_trading_alert = False
        last_day = today

    # שליחת הודעת התחלה
    if not sent_today_start and current_hour == START_HOUR and current_minute == START_MINUTE:
        send_start_message()
        sent_today_start = True

    # שליחת הודעת סיום
    if not sent_today_end and current_hour == END_HOUR and current_minute == END_MINUTE:
        send_end_message()
        sent_today_end = True

    # שליחת התראה אם אין מסחר בפועל
    if not sent_no_trading_alert and is_no_real_trading():
        send_no_real_trading_alert()
        sent_no_trading_alert = True

    # שליחת איתות יומי לפי שעה דינמית
    market_close_hour = get_market_close_hour(today)
    if not sent_today_signal and current_hour == market_close_hour and current_minute == 40:
        send_final_signal()
        sent_today_signal = True

    # שליחת התראת מאקרו לפני
    if not sent_macro_before:
        event_time = now.replace(hour=MACRO_EVENT_HOUR,
                                 minute=MACRO_EVENT_MINUTE,
                                 second=0,
                                 microsecond=0)
        if now >= event_time - timedelta(
                hours=1) and now < event_time - timedelta(minutes=59):
            send_macro_event_summary_before("התראת מאקרו חשובה")
            sent_macro_before = True

    # שליחת סיכום מאקרו אחרי
    if not sent_macro_after:
        event_time = now.replace(hour=MACRO_EVENT_HOUR,
                                 minute=MACRO_EVENT_MINUTE,
                                 second=0,
                                 microsecond=0)
        if now >= event_time + timedelta(
                minutes=15) and now < event_time + timedelta(minutes=16):
            send_macro_event_summary_after("סיכום מאקרו")
            sent_macro_after = True

    time.sleep(60)

send_start_message()
