
import os
from datetime import datetime
from config import DISCORD_PUBLIC_WEBHOOK_URL, DISCORD_PRIVATE_WEBHOOK_URL, DISCORD_ERROR_WEBHOOK_URL
import requests

def get_stock_list():
    from stock_list import STOCKS
    return STOCKS

# שליחת הודעה לדיסקורד
def send_discord_message(webhook_url, message):
    try:
        data = {"content": message}
        requests.post(webhook_url, json=data)
    except Exception as e:
        print(f"שגיאה בשליחת הודעה לדיסקורד: {e}")

# אירועי היום (ללוח שנה כלכלי)
def get_today_events():
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        with open("data/events.json", "r") as f:
            events = f.read()
            return today in events
    except:
        return False

# אירועים קרובים
def get_upcoming_events():
    try:
        with open("data/upcoming_events.json", "r") as f:
            events = f.read()
            return events
    except:
        return ""

# בדיקה אם כבר נשלחה הודעה על חג
def already_sent_holiday_message():
    return os.path.exists("sent_holiday_log.txt")

# סימון שנשלחה הודעה על חג
def mark_holiday_message_sent():
    with open("sent_holiday_log.txt", "w") as f:
        f.write("sent")

# שליחת שגיאה לדיסקורד
def send_error_to_discord(error_message):
    send_discord_message(DISCORD_ERROR_WEBHOOK_URL, f"שגיאת מערכת:\n```{error_message}```")

