import os
import requests

def send_public_message(message):
    webhook_url = os.getenv("DISCORD_PUBLIC_WEBHOOK_URL")
    if webhook_url:
        try:
            requests.post(webhook_url, json={"content": message})
        except Exception as e:
            print(f"שגיאה בשליחת הודעה פומבית: {e}")
