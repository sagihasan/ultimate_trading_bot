import requests
import json
from config import DISCORD_PUBLIC_WEBHOOK, DISCORD_PRIVATE_WEBHOOK, DISCORD_ERROR_WEBHOOK

def send_discord_message(webhook_url, content):
    try:
        data = {"content": content}
        response = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
        if response.status_code != 204:
            print(f"שגיאה בשליחת הודעה לדיסקורד: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"שגיאה כללית בשליחת הודעה: {str(e)}")

def send_public_log(message):
    send_discord_message(DISCORD_PUBLIC_WEBHOOK, message)

def send_private_log(message):
    send_discord_message(DISCORD_PRIVATE_WEBHOOK, message)

def send_error_log(message):
    send_discord_message(DISCORD_ERROR_WEBHOOK, f"שגיאה:\n{message}")

def get_upcoming_events():
    """
    מחזירה רשימה של אירועים כלכליים קרובים בפורמט:
    [{"title": "CPI", "time": datetime_object, "impact": "High"}, ...]
    כרגע הפונקציה מחזירה רשימת דוגמה לצורכי בדיקה
    """
    from datetime import datetime, timedelta

    now = datetime.now()
    example_event = {
        "title": "נאום הפד",
        "time": now.replace(hour=17, minute=0, second=0, microsecond=0),
        "impact": "High"
    }
    return [example_event]

