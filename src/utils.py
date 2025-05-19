# utils.py

from datetime import datetime
import pytz

TIMEZONE = "Asia/Jerusalem"

def get_current_time():
    return datetime.now(pytz.timezone(TIMEZONE))

def format_time(dt=None):
    if dt is None:
        dt = get_current_time()
    return dt.strftime("%Y-%m-%d %H:%M")

def is_weekend(date=None):
    if date is None:
        date = get_current_time()
    return date.weekday() >= 5  # 5 = שבת, 6 = ראשון

def percent(value, total):
    try:
        return round((value / total) * 100, 2)
    except ZeroDivisionError:
        return 0.0

def risk_reward_ratio(risk, reward):
    try:
        return round(reward / risk, 2)
    except ZeroDivisionError:
        return float('inf')

def is_market_open():
    now = get_current_time()
    return now.weekday() < 5 and now.hour >= 15 and now.hour <= 23

def current_date():
    return get_current_time().date()

def current_time_str():
    return get_current_time().strftime("%H:%M")

def short_date():
    return get_current_time().strftime("%Y-%m-%d")

def log(message):
    timestamp = format_time()
    print(f"[{timestamp}] {message}")
