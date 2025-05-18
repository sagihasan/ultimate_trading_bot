# discord_manager.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()

# הגדרת Webhooks מה־.env
PUBLIC_WEBHOOK = os.getenv("DISCORD_PUBLIC_WEBHOOK")
PRIVATE_WEBHOOK = os.getenv("DISCORD_PRIVATE_WEBHOOK")
ERROR_WEBHOOK = os.getenv("DISCORD_ERROR_WEBHOOK")

# שליחת הודעה לדיסקורד
def send_discord_message(message, is_error=False, is_private=False, file=None):
    try:
        if is_error:
            url = ERROR_WEBHOOK
        elif is_private:
            url = PRIVATE_WEBHOOK
        else:
            url = PUBLIC_WEBHOOK

        if not url:
            print("לא מוגדר Webhook לשליחה")
            return

        if file:
            with open(file, "rb") as f:
                requests.post(url, files={"file": f})
        else:
            payload = {"content": message}
            requests.post(url, json=payload)

    except Exception as e:
        print(f"שגיאה בשליחת הודעה לדיסקורד: {e}")

# שליחת שגיאה
def send_error_message(message):
    send_discord_message(f"**שגיאת מערכת:** {message}", is_error=True)
