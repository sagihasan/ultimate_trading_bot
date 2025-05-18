import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Webhooks מקובץ .env
PUBLIC_WEBHOOK = os.getenv("DISCORD_PUBLIC_WEBHOOK")
PRIVATE_WEBHOOK = os.getenv("DISCORD_PRIVATE_WEBHOOK")
ERROR_WEBHOOK = os.getenv("DISCORD_ERROR_WEBHOOK")

# שליחת הודעה לדיסקורד
def send_discord_message(message, is_error=False, is_private=False, file=None):
    try:
        if is_error:
            url = ERROR_WEBHOOK
        elif is_private:
            url = PRIVATE_WEBHOOK
        else:
            url = PUBLIC_WEBHOOK

        if not url:
            print("שגיאה: Webhook לא מוגדר")
            return

        if file:
            with open(file, "rb") as f:
                requests.post(url, files={"file": f})
        else:
            payload = {"content": message}
            requests.post(url, json=payload)

    except Exception as e:
        print(f"שגיאה בשליחת ההודעה לדיסקורד: {e}")

def send_error_message(message):
    send_discord_message(message, is_error=True)

# יצירת הודעת איתות מעוצבת
def create_signal_message(signal_data):
    return f"""
איתות מסחר חכם עבור מניית {signal_data['ticker']}

● כיוון: {signal_data['direction']}
● סוג פקודה: {signal_data['order_type']}
● מחיר כניסה: {signal_data['entry_price']}
● סטופ לוס: {signal_data['stop_loss']}
● טייק פרופיט: {signal_data['take_profit']}

● מגמה טכנית: {signal_data['trend']}
● אזור אסטרטגי: {signal_data['zones']}
● רמת הסיכון: {signal_data['risk_percent']}% ({signal_data['risk_dollars']}$)
● פוטנציאל רווח: {signal_data['reward_percent']}% ({signal_data['reward_dollars']}$)

● אינדיקטור AI: {signal_data['ai_score']}
● Confidence: {signal_data['confidence']}

הבוט קובע: {signal_data['bot_decision']}
"""
