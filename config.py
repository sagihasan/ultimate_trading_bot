# config.py

from datetime import datetime

# ניהול סיכונים
DEFAULT_STOP_LOSS_PERCENT = 3
DEFAULT_TAKE_PROFIT_PERCENT = 6

# זיהוי פערי שעון (DST)
def is_dst_period():
    today = datetime.today()
    dst_start = datetime(today.year, 3, 10)
    dst_end = datetime(today.year, 11, 5)
    return dst_start <= today <= dst_end

USE_DST_MODE = is_dst_period()

# שעות מסחר (שעון ישראל)
MARKET_OPEN_TIME = "15:30" if USE_DST_MODE else "16:30"
MARKET_CLOSE_TIME = "21:30" if USE_DST_MODE else "22:30"
MARKET_CLOSE_SHORT_DAY = "20:00"

# שעות פרה ואפטר מרקט
PRE_MARKET_START = "11:00"
AFTER_MARKET_START = "22:30" if USE_DST_MODE else "23:00"
AFTER_MARKET_END = "02:00"

# זמני איתותים ודוחות
DAILY_SIGNAL_TIME = "21:40" if USE_DST_MODE else "22:40"
WEEKLY_REPORT_DAY = 6  # שבת
WEEKLY_REPORT_HOUR = 12
MONTHLY_REPORT_DAY = 1
MONTHLY_REPORT_HOUR = 12

# Webhooks – נטענים מקובץ .env
DISCORD_PUBLIC_WEBHOOK_URL = None
DISCORD_PRIVATE_WEBHOOK_URL = None
DISCORD_ERROR_WEBHOOK_URL = None"

