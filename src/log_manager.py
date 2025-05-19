import pandas as pd
from datetime import datetime
import os

# קובץ יומן איתותים
LOG_FILE = "data/trades_log.xlsx"

def log_trade(data):
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
