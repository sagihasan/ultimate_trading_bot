# run_all.py

from main import run_bot
from reporting import send_monthly_report_if_needed, send_weekly_report
from keep_alive import keep_alive
from scheduler import start_scheduler

if __name__ == "__main__":
    # שמירת חיבור חי (אם נדרש)
    keep_alive()

    # התחלת סקדולר (משימות מתוזמנות)
    start_scheduler()

    # הרצת הבוט הראשי (איתותים, ניתוחים וכו')
    run_bot()

    # שליחת דוחות
    send_monthly_report_if_needed()
    send_weekly_report()
