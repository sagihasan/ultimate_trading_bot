from datetime import datetime
from src.discord_manager import send_private_message
import time

# הגדרות שעות שליחה (שעון ישראל)
START_HOUR = 11
END_HOUR = 2
END_MINUTE = 10

sent_today_start = False
sent_today_end = False
last_day = None

def daily_schedule_loop():
    global sent_today_start, sent_today_end, last_day

    while True:
        now = datetime.now()
        current_hour = now.hour
        current_minute = now.minute

        if last_day != now.date():
            sent_today_start = False
            sent_today_end = False
            last_day = now.date()

        if not sent_today_start and current_hour == START_HOUR and current_minute == 0:
            send_private_message(f"הבוט התחיל לפעול - {now.strftime('%Y-%m-%d %H:%M')}")
            sent_today_start = True

        if not sent_today_end and current_hour == END_HOUR and current_minute == END_MINUTE:
            send_private_message(f"הבוט סיים את הפעולה - {now.strftime('%Y-%m-%d %H:%M')}")
            sent_today_end = True

        time.sleep(60)
