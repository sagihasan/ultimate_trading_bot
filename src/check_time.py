from datetime import datetime
import pytz

# זמן ברירת מחדל (UTC)
print("UTC:", datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

# זמן ישראל
israel_time = datetime.now(pytz.timezone('Asia/Jerusalem'))
print("שעון ישראל:", israel_time.strftime('%Y-%m-%d %H:%M:%S'))
