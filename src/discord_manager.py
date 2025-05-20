import os
import requests
import time
from utils import send_message_with_delay
from messaging import send_public_message

def send_trade_update_message(message, delay=1.2):
    """
    שולח הודעת עדכון על עסקה לערוץ הדיסקורד הציבורי.
    """
    try:
        send_message_with_delay(send_public_message, message, delay)
    except Exception as e:
        print(f"שגיאה בשליחת עדכון העסקה: {e}")

def send_message_with_delay(send_func, content, delay_seconds=2):
    try:
        send_func(content)
        time.sleep(delay_seconds)
    except Exception as e:
        print(f"שגיאה בשליחת הודעה בעיכוב: {e}")

def send_public_message(content):
    webhook_url = os.getenv("DISCORD_PUBLIC_WEBHOOK")
    if webhook_url:
        try:
            response = requests.post(webhook_url, json={"content": content})
            if response.status_code != 204:
                print(f"שגיאה בשליחת הודעה ציבורית: {response.status_code} {response.text}")
        except Exception as e:
            print(f"שגיאה בשליחת הודעה ציבורית: {e}")
    else:
        print("Webhook ציבורי לא מוגדר")

def send_private_message(content):
    webhook_url = os.getenv("DISCORD_PRIVATE_WEBHOOK")
    if webhook_url:
        try:
            response = requests.post(webhook_url, json={"content": content})
            if response.status_code != 204:
                print(f"שגיאה בשליחת הודעה פרטית: {response.status_code} {response.text}")
        except Exception as e:
            print(f"שגיאה בשליחת הודעה פרטית: {e}")
    else:
        print("Webhook פרטי לא מוגדר")

def send_error_message(error_msg):
    webhook_url = os.getenv("DISCORD_ERROR_WEBHOOK") or os.getenv("DISCORD_PRIVATE_WEBHOOK")
    bot_name = os.getenv("BOT_NAME", "Trading Bot")

    if webhook_url:
        message = f"**שגיאת מערכת – {bot_name}:**\n```{error_msg}```"
        try:
            response = requests.post(webhook_url, json={"content": message})
            if response.status_code != 204:
                print(f"שגיאה בשליחת הודעת שגיאה: {response.status_code}")
        except Exception as e:
            print(f"שגיאה בשליחת הודעת שגיאה: {e}")
    else:
        print("Webhook לשגיאות לא מוגדר")

def create_signal_message(**kwargs):
    # פונקציה ליצירת הודעת איתות – מותאם לפי ערכים
    message = "**איתות חדש לזמן אמת:**\n"
    for key, value in kwargs.items():
        message += f"{key}: {value}\n"
    return message
