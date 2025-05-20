import os
from utils import send_message_with_delay
from dotenv import load_dotenv
import requests

load_dotenv()

# קצב שליחה – שיהיה לפחות 1.2 שניות בין כל הודעה
RATE_LIMIT_SECONDS = 1.2

# Webhook ציבורי ודיסקרטי
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
DISCORD_PRIVATE_WEBHOOK_URL = os.getenv("DISCORD_PRIVATE_WEBHOOK_URL")


def send_public_message(message):
    """
    שליחת הודעה לערוץ הציבורי בדיסקורד.
    """
    if not DISCORD_WEBHOOK_URL:
        print("שגיאה: DISCORD_WEBHOOK_URL לא הוגדר.")
        return
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print(f"שגיאה בשליחת הודעה ציבורית: {e}")


def send_private_message(message):
    """
    שליחת הודעה לערוץ הפרטי בדיסקורד.
    """
    if not DISCORD_PRIVATE_WEBHOOK_URL:
        print("שגיאה: DISCORD_PRIVATE_WEBHOOK_URL לא הוגדר.")
        return
    try:
        requests.post(DISCORD_PRIVATE_WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print(f"שגיאה בשליחת הודעה פרטית: {e}")


def send_error_message(message):
    """
    שליחת הודעת שגיאה לערוץ הפרטי בדיסקורד.
    """
    error_message = f"שגיאה בבוט:\n{message}"
    send_private_message(error_message)


def send_trade_update_message(message, delay=RATE_LIMIT_SECONDS):
    """
    שולח הודעת עדכון על עסקה לערוץ הדיסקורד הציבורי.
    """
    try:
        send_message_with_delay(send_public_message, message, delay)
    except Exception as e:
        print(f"שגיאה בשליחת עדכון העסקה: {e}")
