import os
import requests
from datetime import datetime, timedelta
from discord_manager import send_error_message
from messaging import send_message

def check_macro_alerts():
    try:
        events = [
            {"title": "נאום פאוול", "time": "15:30", "impact": "חזק"},
            {"title": "מדד CPI", "time": "14:00", "impact": "בינוני"},
        ]

        now = datetime.now()
        upcoming = []

        for event in events:
            event_hour = int(event["time"].split(":")[0])
            if now.hour + 1 == event_hour:
                upcoming.append(event)

        for e in upcoming:
            msg = f"""**התראה מקרו קרובה**
אירוע: {e['title']}
שעה: {e['time']}
דרגת השפעה: {e['impact']}
הבוט ממליץ להיות דרוך – ייתכן תנודתיות בשוק
"""
            send_message_with_delay(send_public_message, message)

    except Exception as e:
        send_error_message(f"שגיאה בבדיקת מקרו: {e}")
