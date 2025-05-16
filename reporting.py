# reporting.py

from datetime import datetime
from report_generator import generate_monthly_report
from discord_manager import send_discord_message

def send_monthly_report_if_needed():
    now = datetime.now()
    if now.day == 1 and now.hour == 12:
        report = generate_monthly_report()
        send_discord_message(report, is_private=True)

def send_weekly_report():
    today = datetime.today()
    if today.weekday() == 6 and today.hour == 12:
        send_discord_message("**דו״ח שבועי:** יתפרסם בהמשך (ממתין לחיבור מלא ל־weekly_forecast).", is_private=True)
