# log_manager.py

from datetime import datetime
import traceback

LOG_FILE = "logs/error_log.txt"

def log_error(error_message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {error_message}\n"
    print(full_message)

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(full_message)
    except Exception as e:
        print(f"שגיאה בשמירת הלוג: {e}")

def log_exception(e):
    tb = traceback.format_exc()
    log_error(f"{str(e)}\n{tb}")
