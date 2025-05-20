import os
import requests
import time

RATE_LIMIT_SECONDS = 1.2
DISCORD_PUBLIC_WEBHOOK = os.getenv("DISCORD_PUBLIC_WEBHOOK")

def send_message(webhook_url, message):
    if not webhook_url:
        print("לא הוגדרה כתובת webhook")
        return
    try:
        response = requests.post(webhook_url, json={"content": message})
        if response.status_code == 429:
            print("Rate limit – ההודעה נדחתה זמנית")
        elif not response.ok:
            print(f"שגיאה בשליחה: {response.status_code}")
    except Exception as e:
        print(f"שגיאה בשליחה לדיסקורד: {e}")

def send_public_message(message):
    send_message(DISCORD_PUBLIC_WEBHOOK_URL, message)

def send_message_with_delay(func, message, delay=RATE_LIMIT_SECONDS):
    time.sleep(delay)
    func(message)
