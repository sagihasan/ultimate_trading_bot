from datetime import datetime
from discord_manager import send_error_message

def log_error(error_message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] שגיאה: {error_message}"
    print(full_message)
    send_error_message(full_message)
