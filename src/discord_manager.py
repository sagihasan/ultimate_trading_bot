import os
from utils import send_message_with_delay
from dotenv import load_dotenv
import requests

load_dotenv()
# ייבוא קבועים מתוך .env
DISCORD_PRIVATE_WEBHOOK = os.getenv("DISCORD_PRIVATE_WEBHOOK")
DISCORD_ERROR_WEBHOOK_URL = os.getenv("DISCORD_ERROR_WEBHOOK_URL")

# הגדרת הגבלת קצב לשליחת הודעות
RATE_LIMIT_SECONDS = 1.2

def send_message_with_delay(send_func, message, delay=RATE_LIMIT_SECONDS):
    time.sleep(delay)
    send_func(message)

def send_private_message(message, delay=RATE_LIMIT_SECONDS):
    """
    שולח הודעה לערוץ דיסקורד פרטי (למשל עבור עדכונים אישיים).
    """
    try:
        if DISCORD_PRIVATE_WEBHOOK:
            payload = {"content": message}
            response = requests.post(DISCORD_PRIVATE_WEBHOOK, json=payload)
            if response.status_code != 204:
                print(f"שגיאה בשליחת הודעה פרטית: {response.status_code} {response.text}")
    except Exception as e:
        print(f"שגיאה בשליחת הודעה פרטית: {e}")

def send_error_message(error_message, delay=RATE_LIMIT_SECONDS):
    """
    שולח הודעת שגיאה לערוץ דיסקורד ייעודי לשגיאות.
    """
    try:
        if DISCORD_ERROR_WEBHOOK_URL:
            payload = {"content": f"**שגיאת בוט:**\n{error_message}"}
            response = requests.post(DISCORD_ERROR_WEBHOOK_URL, json=payload)
            if response.status_code != 204:
                print(f"שגיאה בשליחת הודעת שגיאה: {response.status_code} {response.text}")
    except Exception as e:
        print(f"שגיאה בשליחת הודעת שגיאה: {e}")

def send_trade_update_message(message, delay=RATE_LIMIT_SECONDS):
    """
    שולח הודעת עדכון על עסקה לערוץ הפרטי.
    """
    try:
        send_message_with_delay(send_private_message, message, delay)
    except Exception as e:
        print(f"שגיאה בשליחת עדכון העסקה: {e}")
