# run_all.py

from main import run_bot
from reporting import send_monthly_report_if_needed, send_weekly_report
from keep_alive import keep_alive
from scheduler import start_scheduler

if __name__ == "__main__":
    # הרצה מתמשכת (שרת Flask)
    keep_alive()

    # הפעלת Scheduler לזימונים יומיים/שבועיים
    start_scheduler()

    # הפעלת בוט מסחר יומית
    run_bot()

    # שליחת דוח חודשי אם היום הראשון בחודש
    send_monthly_report_if_needed()

    # שליחת דוח שבועי אם שבת
    send_weekly_report()
