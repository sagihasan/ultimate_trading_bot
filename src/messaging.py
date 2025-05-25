import os
import requests

from env_loader import (
    DISCORD_PUBLIC_WEBHOOK_URL,
    DISCORD_PRIVATE_WEBHOOK_URL,
    DISCORD_ERRORS_WEBHOOK_URL
)

def send_message(webhook_url, content):
    try:
        data = {"content": content}
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
    except Exception as e:
        print(f"שגיאה בשליחת הודעה לדיסקורד: {e}")

def send_public_message(content):
    send_message(DISCORD_PUBLIC_WEBHOOK_URL, content)

def send_private_message(content):
    send_message(DISCORD_PRIVATE_WEBHOOK_URL, content)

def send_error_message(content):
    send_message(DISCORD_ERRORS_WEBHOOK_URL, content)
