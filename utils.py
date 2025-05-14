
import os
import json
from datetime import datetime, timedelta
import requests
from config import DISCORD_ERROR_WEBHOOK

def send_discord_message(webhook_url, message):
    try:
        data = {"content": message}
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
    except Exception as e:
        print(f"שגיאה בשליחת הודעה לדיסקורד: {e}")

def get_today_events():
    path = "data/events/today_events.json"
    if not os.path.exists(path):
        return []
    with open(path, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def get_upcoming_events():
    path = "data/events/upcoming_events.json"
    if not os.path.exists(path):
        return []
    with open(path, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def already_sent_log(file_name, message_id):
    if not os.path.exists(file_name):
        return False
    with open(file_name, "r") as f:
        return message_id in f.read()

def mark_log_as_sent(file_name, message_id):
    with open(file_name, "a") as f:
        f.write(f"{message_id}\n")

def already_sent_holiday_message():
    return False  # future implementation

