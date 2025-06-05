import subprocess
import threading
from keep_alive import keep_alive
from scheduler import start_scheduler
from monthly_planner import send_monthly_plan
from reporting import send_monthly_report_if_needed, send_weekly_report_if_needed
from messaging import send_message
from discord_manager import DISCORD_PUBLIC_WEBHOOK_URL, DISCORD_PRIVATE_WEBHOOK_URL, DISCORD_ERRORS_WEBHOOK_URL

# הפעלת loop יומי לדוחות או הודעות אם צריך
def run_main_py():
    subprocess.run(["python3", "main_loop.py"])


if __name__ == "__main__":
    # 🟢 שליחת הודעת התחלה + הודעת סיום + איתותים (main.py)
    threading.Thread(target=run_main.py, daemon=True).start()

    # 🟢 שמירה על הרצה תמידית ב־Replit
    keep_alive()

    # 🟢 הפעלת Scheduler לדוחות, ניתוחים ואירועים
    start_scheduler()

    # 🟢 שליחת דוחות אם צריך
    send_weekly_report_if_needed()
    send_monthly_report_if_needed()

    # 🟢 שליחת תכנון חודשי
    send_monthly_plan()
