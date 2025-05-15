
import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime
import time
import json
from config import DISCORD_ERROR_WEBHOOK

last_sent_times = {}
HOLIDAY_LOG_FILE = "sent_holiday_log.txt"

# שליחת הודעה לדיסקורד עם בקרת תדירות
def send_discord_message(webhook_url, message, message_type="default"):
    try:
        key = f"{webhook_url}_{message_type}"
        now = time.time()

        if key in last_sent_times and now - last_sent_times[key] < 15:
            return

        data = {"content": message}
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        last_sent_times[key] = now
    except Exception as e:
        print(f"שגיאה בשליחה לדיסקורד: {e}")

# בדיקת הודעת חג
def already_sent_holiday_message(date_str):
    if not os.path.exists(HOLIDAY_LOG_FILE):
        return False
    with open(HOLIDAY_LOG_FILE, "r") as f:
        sent = json.load(f)
    return sent.get(date_str, False)

def mark_holiday_message_sent(date_str):
    if os.path.exists(HOLIDAY_LOG_FILE):
        with open(HOLIDAY_LOG_FILE, "r") as f:
            sent = json.load(f)
    else:
        sent = {}
    sent[date_str] = True
    with open(HOLIDAY_LOG_FILE, "w") as f:
        json.dump(sent, f)

# שמירה לאקסל
def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

# טעינת עסקאות
def load_trade_data():
    if os.path.exists("signals_log.xlsx"):
        return pd.read_excel("signals_log.xlsx").to_dict(orient="records")
    return []

def load_open_trades():
    if os.path.exists("open_trades.xlsx"):
        return pd.read_excel("open_trades.xlsx").to_dict(orient="records")
    return []

# זיהוי אירועים כלכליים (פיקטיבי לדוגמה – אפשר לחבר ל־Investing בעתיד)
def get_today_events():
    sample_events = [
        {"time": "17:00", "description": "נאום פאוול"},
        {"time": "15:30", "description": "נתוני CPI"}
    ]
    now = datetime.now().strftime("%H:%M")
    return [e for e in sample_events if e["time"] >= now]

