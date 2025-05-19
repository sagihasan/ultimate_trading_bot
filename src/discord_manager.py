import os
import requests

def send_public_message(content):
    webhook_url = os.getenv("DISCORD_PUBLIC_WEBHOOK")
    if webhook_url:
        try:
            response = requests.post(webhook_url, json={"content": content})
            if response.status_code != 204:
                print(f"שגיאה בשליחה לציבורי: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"שגיאה בשליחה לציבורי: {e}")
    else:
        print("לא נמצא Webhook ציבורי")

def send_private_message(content):
    webhook_url = os.getenv("DISCORD_PRIVATE_WEBHOOK")
    if webhook_url:
        try:
            response = requests.post(webhook_url, json={"content": content})
            if response.status_code != 204:
                print(f"שגיאה בשליחה לפרטי: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"שגיאה בשליחה לפרטי: {e}")
    else:
        print("לא נמצא Webhook פרטי")

def send_error_message(error_msg):
    webhook_url = os.getenv("DISCORD_ERROR_WEBHOOK") or os.getenv("DISCORD_PRIVATE_WEBHOOK")
    bot_name = os.getenv("BOT_NAME", "Trading Bot")
    if webhook_url:
        message = f"**{bot_name} - שגיאת מערכת:**/n"
        message = f"```{error_msg}```"
        try:
            response = requests.post(webhook_url, json={"content": message})
            if response.status_code != 204:
                print(f"שגיאה בשליחת הודעת שגיאה: {response.status_code}")
        except Exception as e:
            print(f"שגיאה בשליחת שגיאה: {e}")
    else:
        print("Webhook שגיאות לא מוגדר")
