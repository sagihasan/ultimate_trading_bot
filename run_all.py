# run_all.py

from main import main
from scheduler import run_scheduler
from utils import get_today_events
from changelog_manager import send_latest_changelog
import threading

if __name__ == "__main__":
    # שליחת העדכון האחרון מה־CHANGELOG
    send_latest_changelog()

    # הפעלת ניהול עסקאות ודוחות ברקע
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    # הרצת הבוט הראשי של האיתות
    main()

    # המתנה לסיום הסקדולר (אופציונלי)
    scheduler_thread.join()
