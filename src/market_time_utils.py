# src/market_time_utils.py

from datetime import time, datetime
import pandas_market_calendars as mcal

# שעת סיום רגילה של מסחר (22:00)
REGULAR_CLOSE = time(22, 0)

# שעת סיום ביום מקוצר (20:00)
SHORT_DAY_CLOSE = time(20, 0)

# תקופות פערי שעון (שעון קיץ/חורף)
def is_dst_gap_period():
    today = datetime.now()
    return (today.month == 3 and today.day >= 10) or (today.month == 11 and today.day <= 10)

def get_market_close_hour(today=None):
    if today is None:
        today = datetime.now()
    if today.weekday() == 4:
        return 0  # אין מסחר
    if is_short_trading_day():
        return 20
    elif is_dst_gap_period():
        return 21
    else:
        return 22

def is_short_trading_day():
    today = datetime.now().date()
    short_days = [
        "2025-11-28",  # יום אחרי חג ההודיה
        "2025-12-24",  # ערב חג המולד
    ]
    return today.strftime("%Y-%m-%d") in short_days

def is_market_closed():
    nyse = mcal.get_calendar('XNYS')
    today = datetime.now().date()
    schedule = nyse.schedule(start_date=today, end_date=today)
    return schedule.empty

def is_real_trading_day():
    return is_trading_day() and not is_market_closed()

def is_no_real_trading():
    # סימולציה אם יש בעיות מסחר (כמו פיקים או ווליום נמוך)
    return False  # אלא אם תוסיף תנאים אמיתיים תמיד false
