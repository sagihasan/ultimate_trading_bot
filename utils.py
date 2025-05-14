import requests
import datetime
import os

# שליחת הודעה לדיסקורד
def send_discord_message(webhook_url, message):
    try:
        data = {"content": message}
        requests.post(webhook_url, json=data)
    except Exception as e:
        print(f"שגיאה בשליחת הודעת דיסקורד: {e}")

# זיהוי אם כבר נשלחה הודעת חג
def already_sent_holiday_message(date_str):
    try:
        with open("sent_holiday_log.txt", "r") as f:
            return date_str in f.read()
    except FileNotFoundError:
        return False

# סימון הודעת חג כשלוחה
def mark_holiday_message_sent(date_str):
    with open("sent_holiday_log.txt", "a") as f:
        f.write(date_str + "\n")

# בדיקת אם היום יום חג לפי לוח NYSE
def is_holiday(date_obj):
    nyse_holidays = [
        "2025-01-01", "2025-01-20", "2025-02-17", "2025-04-18", "2025-05-26",
        "2025-07-04", "2025-09-01", "2025-11-27", "2025-12-25"
    ]
    return date_obj.strftime("%Y-%m-%d") in nyse_holidays

# ניתן להוסיף כאן פונקציות נוספות שקשורות להודעות מערכת

