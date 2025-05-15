# run_all.py
from main import main
from scheduler import run_scheduler
from changelog_manager import send_latest_changelog
import threading
import time
from datetime import datetime
import pytz
from utils import log_to_console

if __name__ == "__main__":
    # שורת פתיחה ב־09:30
    now = datetime.now(pytz.timezone("Asia/Jerusalem"))
    if now.strftime("%H:%M") == "09:30":
        log_to_console("הבוט התעורר. ב־11:00 תישלח הודעת פתיחה.")

    # הפעלת עדכון שוטף ודוחות ברקע
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    # הפעלת הבוט הראשי (איתותים)
    main()

    scheduler_thread.join()
