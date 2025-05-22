# run_all.py

from main import run_bot
from reporting import send_monthly_report_if_needed, send_weekly_report_if_needed
from keep_alive import keep_alive
from scheduler import start_scheduler
from monthly_planner import send_monthly_plan
from src.scheduler_loop import daily_schedule_loop
import threading

if __name__ == "__main__":
    # הפעלת שליחת ההודעות הקבועות ב־11:00 ו־02:10
    threading.Thread(target=daily_schedule_loop, daemon=True).start()

    # הפעלת keep alive
    keep_alive()

    # הפעלת Scheduler לזמנים קבועים (איתותים, ניתוחים, דיווחים)
    start_scheduler()

    # הרצת הבוט הראשי (איתותים, ניתוחים, ניהול עסקאות)
    run_bot()

    # שליחת דוחות
    send_monthly_report_if_needed()
    send_weekly_report_if_needed()

    # שליחת תוכנית חודשית בתחילת כל חודש
    send_monthly_plan()
