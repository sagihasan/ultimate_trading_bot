# discord_manager.py

import requests
import os

# נטען את ה-Webhooks מקובץ .env
PUBLIC_WEBHOOK = os.getenv("DISCORD_PUBLIC_WEBHOOK_URL")
PRIVATE_WEBHOOK = os.getenv("DISCORD_PRIVATE_WEBHOOK_URL")
ERROR_WEBHOOK = os.getenv("DISCORD_ERROR_WEBHOOK_URL")

def send_discord_message(message, is_private=False, is_error=False, file=None):
    try:
        url = ERROR_WEBHOOK if is_error else PRIVATE_WEBHOOK if is_private else PUBLIC_WEBHOOK
        if not url:
            print("לא הוגדר Webhook לשליחה")
            return

        if file:
            requests.post(url, files={"file": file})
        else:
            payload = {"content": message}
            requests.post(url, json=payload)

    except Exception as e:
        print(f"שגיאה בשליחת הודעה לדיסקורד: {e}")

def send_error_message(message):
    send_discord_message(f"**שגיאת מערכת:**\n{message}", is_error=True)
