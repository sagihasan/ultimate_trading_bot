import os
import requests
from dotenv import load_dotenv

# טוען משתני סביבה
load_dotenv()

# שליפה של הכתובות מהקובץ .env
PUBLIC = os.getenv("DISCORD_PUBLIC_WEBHOOK_URL")
PRIVATE = os.getenv("DISCORD_PRIVATE_WEBHOOK_URL")
ERRORS = os.getenv("DISCORD_ERRORS_WEBHOOK_URL")

def send_message(url, content):
    if url:
        try:
            response = requests.post(url, json={"content": content})
            if response.status_code == 204:
                print(f"הודעה נשלחה בהצלחה לכתובת: {url}")
            else:
                print(f"שגיאה בשליחה ל־{url}: {response.status_code}")
        except Exception as e:
            print(f"תקלה בשליחה ל־{url}:\n{e}")

# שליחת הודעות בדיקה
send_message(PUBLIC, "📢 בדיקת שליחה לערוץ **ציבורי** בוצעה בהצלחה.")
send_message(PRIVATE, "📥 בדיקת שליחה לערוץ **פרטי** בוצעה בהצלחה.")
send_message(ERRORS, "⚠️ בדיקת שליחה לערוץ **שגיאות** בוצעה בהצלחה.")
