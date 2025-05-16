# run_all.py

from main import run_bot
from reporting import send_monthly_report_if_needed, send_weekly_report
from keep_alive import keep_alive

if __name__ == "__main__":
    # שומר על הבוט חי כל הזמן (Render / Replit)
    keep_alive()

    # הפעלת הבוט היומי: איתותים, ניתוחים, ניהול עסקאות
    run_bot()

    # שליחת דו"ח חודשי – אם היום זה ה־1 לחודש ב־12:00
    send_monthly_report_if_needed()

    # שליחת דו"ח שבועי – אם היום זה יום ראשון ב־12:00
    send_weekly_report()
