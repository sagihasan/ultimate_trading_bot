
import requests
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_PUBLIC_WEBHOOK_URL = os.getenv("DISCORD_PUBLIC_WEBHOOK_URL")
DISCORD_PRIVATE_WEBHOOK_URL = os.getenv("DISCORD_PRIVATE_WEBHOOK_URL")
DISCORD_ERROR_WEBHOOK_URL = os.getenv("DISCORD_ERROR_WEBHOOK_URL")

def send_message(webhook_url, message):
    try:
        data = {"content": message}
        response = requests.post(webhook_url, json=data)
        if response.status_code != 204:
            print(f"שגיאה בשליחת הודעה לדיסקורד: {response.status_code} | {response.text}")
    except Exception as e:
        print(f"שגיאה כללית בשליחת הודעה לדיסקורד: {str(e)}")
