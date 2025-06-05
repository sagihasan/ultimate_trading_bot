import os
import requests

from env_loader import (DISCORD_PUBLIC_WEBHOOK_URL,
                        DISCORD_PRIVATE_WEBHOOK_URL,
                        DISCORD_ERRORS_WEBHOOK_URL)


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


def send_macro_event_summary_before(event, strength, time):
    print(f"📢 תזכורת לאירוע מקרו חזק ({strength}) בעוד שעה ב־{time}: {event}")
    # כאן אפשר להוסיף שליחה לדיסקורד


def send_macro_event_summary_after(event, summary):
    print(f"📢 סיכום לאחר האירוע {event}: {summary}")
    # כאן אפשר להוסיף שליחה לדיסקורד

def send_start_message():
    send_message(DISCORD_PRIVATE_WEBHOOK_URL, "🟢 הבוט התחיל לפעול.")

def send_end_message():
    send_message(DISCORD_PRIVATE_WEBHOOK_URL, "🌙 הבוט סיים לפעול.")
