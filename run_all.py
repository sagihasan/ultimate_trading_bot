# run_all.py – קובץ הרצה כולל של הבוט

from main import main
from scheduler import run_scheduler
from changelog_manager import send_latest_changelog
import threading
import time
from datetime import datetime
import pytz
from config import DISCORD_PRIVATE_WEBHOOK
from utils import send_discord_message

def log_startup_messages():
    jerusalem = pytz.timezone("Asia/Jerusalem")
    now = datetime.now(jerusalem)
    hour = now.hour
    minute = now.minute

    if hour == 9 and minute == 30:
        print("הבוט התעורר – ב־11:00 תישלח הודעת פתיחה.")
    elif hour == 11 and minute == 0:
        print("הבוט התחיל לפעול – בדוק בערוץ הפרטי.")
    elif hour == 11 and minute == 10:
        print("הבוט התחיל לבדוק את הפרי-מרקט.")
    elif hour == 15 and minute == 30:
        print("פערי שעון: הבוט התחיל את המסחר.")
    elif hour == 16 and minute == 30:
        print("הבוט התחיל את המסחר – ישלח איתות בערב.")
    elif hour == 19 and minute == 40:
        print("חצי יום: הבוט ישלח איתות עכשיו.")
    elif hour == 21 and minute == 40:
        print("פערי שעון: הבוט ישלח איתות עכשיו.")
    elif hour == 22 and minute == 40:
        print("הבוט ישלח איתות עכשיו.")
    elif hour == 23 and minute == 10:
        print("הבוט התחיל את האפטר-מרקט.")
    elif hour == 2 and minute == 0:
        print("02:00 – הבוט סיים לפעול.")

def run_all():
    # שליחת CHANGELOG פעם ביום ראשון ב־11:00
    now = datetime.now(pytz.timezone("Asia/Jerusalem"))
    if now.weekday() == 6 and now.hour == 11 and now.minute == 0:
        send_latest_changelog()

    # שליחת הודעת התחלה פרטית
    if now.hour == 11 and now.minute == 0:
        send_discord_message(DISCORD_PRIVATE_WEBHOOK, "הבוט התחיל לפעול – בדוק בערוץ הפרטי.", message_type="log")

    # הדפסת הודעה מקומית לפי שעה
    log_startup_messages()

    # הרצת ניהול עסקאות ודוחות ברקע
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    # הרצת הבוט הראשי של האיתות
    main()

    # ממתין לסיום של scheduler אם נדרש
    scheduler_thread.join()

if __name__ == "__main__":
    run_all()
