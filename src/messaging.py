import requests
import time

# שמור זמן שליחה אחרון עבור כל webhook
last_sent_times = {}

def send_message(webhook_url, message):
    try:
        # אם כבר נשלחה הודעה ל־webhook הזה — המתן לפחות 1.5 שניות מהפעם הקודמת
        now = time.time()
        last_time = last_sent_times.get(webhook_url, 0)
        if now - last_time < 1.5:
            time.sleep(1.5 - (now - last_time))

        data = {"content": message}
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()

        # עדכן זמן שליחה אחרון
        last_sent_times[webhook_url] = time.time()

    except Exception as e:
        print(f"שגיאה בשליחת הודעה לדיסקורד: {e}")
