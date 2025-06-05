# src/market_time_utils.py

from datetime import time, datetime
import pandas_market_calendars as mcal
import yfinance as yf

# שעות סגירה
REGULAR_CLOSE = time(22, 0)      # יום רגיל
SHORT_DAY_CLOSE = time(20, 0)    # יום מסחר מקוצר
DST_CLOSE = time(21, 0)          # שעון חורף/קיץ

# בדיקה אם תקופת פערי שעון
def is_dst_gap_period():
    today = datetime.now()
    return (today.month == 3 and today.day >= 10) or (today.month == 11 and today.day <= 10)

# בדיקת שעת סיום מסחר (22 רגיל, 21 חורף, 20 מקוצר)
def get_market_close_hour(today=None):
    if today is None:
        today = datetime.now()
    if today.weekday() == 4:  # יום שישי
        return 0  # אין מסחר
    if is_short_trading_day():
        return 20
    elif is_dst_gap_period():
        return 21
    else:
        return 22

# בדיקת האם זה יום מסחר מקוצר
def is_short_trading_day():
    today = datetime.now().date()
    short_days = [
        "2025-11-28",  # יום שישי שאחרי חג ההודיה
        "2025-12-24",  # ערב חג המולד
    ]
    return today.strftime("%Y-%m-%d") in short_days

# בדיקת האם בפועל אין מסחר למרות שזה יום מסחר רגיל
def is_no_real_trading():
    """
    אם היום הוא יום מסחר אבל אין מסחר בפועל – כלומר ווליום נמוך מדי ב-SPY.
    """
    now = datetime.now()
    if now.hour < 17:
        return False

    try:
        data = yf.download("SPY", period="1d", interval="1m")
        if data.empty:
            return True
        volume = data["Volume"].sum()
        return volume < 1_000_000
    except Exception as e:
        print(f"שגיאה בבדיקת ווליום SPY: {e}")
        return False

# בדיקה אם זה יום מסחר לפי לוח השנה של הבורסה
def is_trading_day():
    nyse = mcal.get_calendar('XNYS')
    today = datetime.now().date()
    schedule = nyse.schedule(start_date=today, end_date=today)
    return not schedule.empty

# בדיקה אם היום הוא יום מסחר אמיתי (לפי לוח שנה ולפי שאין סגירה)
def is_real_trading_day():
    return is_trading_day() and not is_market_closed()

# בדיקה אם הבורסה סגורה רשמית (חג או אירוע)
def is_market_closed():
    nyse = mcal.get_calendar('XNYS')
    today = datetime.now().date()
    schedule = nyse.schedule(start_date=today, end_date=today)
    return schedule.empty
