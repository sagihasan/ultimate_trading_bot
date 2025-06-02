import pandas as pd
from datetime import datetime
import os
from pytz import timezone

# קובץ יומן איתותים
LOG_FILE = "data/trades_log.xlsx"


def log_trade(data):
    try:
        israel_tz = timezone("Asia/Jerusalem")
        now = datetime.now(israel_tz).strftime("%Y-%m-%d %H:%M:%S")
        data['timestamp'] = now

        if os.path.exists(LOG_FILE):
            df = pd.read_excel(LOG_FILE)
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        else:
            df = pd.DataFrame([data])

        df.to_excel(LOG_FILE, index=False)
        print("עסקה נרשמה בהצלחה.")

    except Exception as e:
        print(f"שגיאה ברישום עסקה: {e}")
