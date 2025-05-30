from messaging import send_message
from env_loader import (
    DISCORD_PUBLIC_WEBHOOK_URL,
    DISCORD_PRIVATE_WEBHOOK_URL,
    DISCORD_ERRORS_WEBHOOK_URL
)

def send_public_message(message):
    send_message(DISCORD_PUBLIC_WEBHOOK_URL, message)

def send_private_message(message):
    send_message(DISCORD_PRIVATE_WEBHOOK_URL, message)

def send_error_message(message):
    send_message(DISCORD_ERRORS_WEBHOOK_URL, f"[שגיאת בוט] {message}")

def send_trade_update_message(message):
    send_message(DISCORD_PUBLIC_WEBHOOK_URL, f"[עדכון עסקה] {message}")
