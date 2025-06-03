import time
import requests
from discord_manager import (
    DISCORD_PUBLIC_WEBHOOK_URL,
    DISCORD_PRIVATE_WEBHOOK_URL,
    DISCORD_ERROR_WEBHOOK_URL
)

def send_message(webhook_url, content):
    response = requests.post(webhook_url, json={"content": content})
    if response.status_code == 204:
        print(f"הודעה נשלחה בהצלחה: {content}")
    else:
        print(f"שגיאה בשליחה: {webhook_url} | קוד: {response.status_code}")

# שליחת הודעה לערוץ הציבורי
send_message(DISCORD_PUBLIC_WEBHOOK_URL, "📢 בדיקת שליחה לערוץ הציבורי")
time.sleep(3)

# שליחת הודעה לערוץ הפרטי
send_message(DISCORD_PRIVATE_WEBHOOK_URL, "🔒 בדיקת שליחה לערוץ הפרטי")
time.sleep(3)

# שליחת הודעה לערוץ השגיאות
send_message(DISCORD_ERROR_WEBHOOK_URL, "❗ בדיקת שליחה לערוץ השגיאות")
time.sleep(3)
