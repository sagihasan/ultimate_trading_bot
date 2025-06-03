from messaging import send_message
import os
from env_loader import load_env

# טוען את כל משתני הסביבה מהקובץ .env
load_env()

# טוען את כל ה־webhooks מהסביבה
public_webhook = os.getenv("DISCORD_PUBLIC_WEBHOOK_URL")
private_webhook = os.getenv("DISCORD_PRIVATE_WEBHOOK_URL")
error_webhook = os.getenv("DISCORD_ERRORS_WEBHOOK_URL")

# שולח הודעות בדיקה לכל הערוצים
send_message(public_webhook, "✅ בדיקת שליחת הודעה לערוץ הציבורי")
time.sleep(3)
send_message(private_webhook, "🔒 בדיקת שליחת הודעה לערוץ הפרטי")
time.sleep(3)
send_message(error_webhook, "🚨 בדיקת שליחת הודעה לערוץ השגיאות")
time.sleep(3)
