import requests
import os

PUBLIC_WEBHOOK_URL = os.getenv("DISCORD_PUBLIC_WEBHOOK_URL")
PRIVATE_WEBHOOK_URL = os.getenv("DISCORD_PRIVATE_WEBHOOK_URL")
ERROR_WEBHOOK_URL = os.getenv("DISCORD_ERROR_WEBHOOK_URL")

def send_discord_message(message: str, is_private: bool = False):
    url = PRIVATE_WEBHOOK_URL if is_private else PUBLIC_WEBHOOK_URL
    if not url:
        print("Discord Webhook URL not found.")
        return
    payload = {"content": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Failed to send message: {e}")

def send_error_message(error_message: str):
    if not ERROR_WEBHOOK_URL:
        print("Error webhook URL not configured.")
        return
    payload = {"content": f"[שגיאה בבוט]: {error_message}"}
    try:
        requests.post(ERROR_WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Failed to send error message: {e}")
