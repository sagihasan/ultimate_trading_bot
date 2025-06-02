import os
import requests
from env_loader import (
    DISCORD_PUBLIC_WEBHOOK_URL,
    DISCORD_PRIVATE_WEBHOOK_URL,
    DISCORD_ERRORS_WEBHOOK_URL,
)


# שליחת הודעה לערוץ הציבורי
def send_public_message(message):
    try:
        response = requests.post(DISCORD_PUBLIC_WEBHOOK_URL,
                                 json={"content": message})
        if response.status_code != 204:
            print(
                f"שגיאה בשליחת הודעה ציבורית: {response.status_code} - {response.text}"
            )
    except Exception as e:
        print(f"שגיאה בעת שליחת הודעה ציבורית: {str(e)}")


# שליחת הודעה לערוץ הפרטי
def send_private_message(message):
    try:
        response = requests.post(DISCORD_PRIVATE_WEBHOOK_URL,
                                 json={"content": message})
        if response.status_code != 204:
            print(
                f"שגיאה בשליחת הודעה פרטית: {response.status_code} - {response.text}"
            )
    except Exception as e:
        print(f"שגיאה בעת שליחת הודעה פרטית: {str(e)}")


# שליחת שגיאה לערוץ השגיאות
def send_error_message(message):
    try:
        response = requests.post(DISCORD_ERRORS_WEBHOOK_URL,
                                 json={"content": message})
        if response.status_code != 204:
            print(
                f"שגיאה בשליחת הודעת שגיאה: {response.status_code} - {response.text}"
            )
    except Exception as e:
        print(f"שגיאה בעת שליחת הודעת שגיאה: {str(e)}")


# שליחת קובץ לערוץ הפרטי (PDF, Excel וכו')
def send_file_to_discord(file_path, message="📄 קובץ צורף על ידי הבוט"):
    try:
        if not os.path.exists(file_path):
            print(f"❌ הקובץ לא נמצא: {file_path}")
            return

        with open(file_path, "rb") as f:
            file_name = os.path.basename(file_path)
            response = requests.post(DISCORD_PRIVATE_WEBHOOK_URL,
                                     data={"content": message},
                                     files={"file": (file_name, f)})

        if response.status_code == 204:
            print(f"✅ הקובץ נשלח בהצלחה: {file_name}")
        else:
            print(
                f"❌ שגיאה בשליחת קובץ: {response.status_code} - {response.text}"
            )

    except Exception as e:
        print(f"❌ שגיאה כללית בשליחת קובץ: {str(e)}")


def send_trade_update_message(message: str):
    try:
        data = {"content": message}
        response = requests.post(DISCORD_PUBLIC_WEBHOOK_URL, json=data)
        response.raise_for_status()
    except Exception as e:
        print(f"שגיאה בשליחת עדכון על עסקה: {e}")
