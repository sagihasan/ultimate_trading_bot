import os
import time
import pytz
from datetime import datetime, timedelta
from dotenv import load_dotenv
from utils import send_discord_message, get_today_events, get_upcoming_events, log_event
from fundamentals import analyze_fundamentals
from technicals import run_technical_analysis
from stock_list import STOCK_LIST
from config import (
    DISCORD_PUBLIC_WEBHOOK_URL, DISCORD_ERROR_WEBHOOK_URL,
    DISCORD_PRIVATE_WEBHOOK_URL, ACCOUNT_SIZE, RISK_PERCENTAGE,
    STOP_LOSS_PERCENT, TAKE_PROFIT_PERCENT
)

load_dotenv()

def is_dst_gap_period(date):
    return date.month == 3 and 10 <= date.day <= 29

def is_half_day():
    return False  # Placeholder. Add logic if needed.

def is_market_day():
    return datetime.now(pytz.timezone("America/New_York")).weekday() < 5

def send_startup_logs():
    now = datetime.now(pytz.timezone("Asia/Jerusalem"))
    if now.strftime("%H:%M") == "11:00":
        print("הבוט התחיל לפעול. מחכה לשעה 22:40")
        send_discord_message(DISCORD_PRIVATE_WEBHOOK_URL, "הבוט התחיל לפעול. מחכה לשעה 22:40")
    elif now.strftime("%H:%M") == "11:10":
        print("הבוט בודק עכשיו את הפרי מארקט")
    elif now.strftime("%H:%M") in ["15:30", "16:30"]:
        print("הבוט סיים לבדוק את הפרי מארקט והתחיל את המסחר. שליחת איתות תהיה בהתאם לשעה שהוגדרה")
    elif now.strftime("%H:%M") in ["19:40", "21:40", "22:40"]:
        print("הבוט שולח איתות. תבדוק את הערוץ הציבורי")
    elif now.strftime("%H:%M") == "23:10":
        print("הבוט סיים את המסחר ומתחיל את האפטר מארקט")
    elif now.strftime("%H:%M") == "02:00":
        print("הבוט סיים לפעול. שלח עדכון יומי לערוץ הפרטי")


def run_bot():
    try:
        now = datetime.now(pytz.timezone("Asia/Jerusalem"))
        send_startup_logs()

        # אירועים כלכליים
        if now.minute == 0:
            log_event("הבוט מחפש אירועים כלכליים")
            upcoming = get_upcoming_events()
            if upcoming:
                for event in upcoming:
                    if event['time'] == (now + timedelta(hours=1)).strftime("%H:%M"):
                        send_discord_message(DISCORD_PUBLIC_WEBHOOK_URL, f"הבוט מצא אירוע כלכלי בשעה {event['time']}. תבדוק את הערוץ הציבורי")
                    if event['time'] == (now - timedelta(minutes=15)).strftime("%H:%M"):
                        send_discord_message(DISCORD_PUBLIC_WEBHOOK_URL, f"האירוע הכלכלי הסתיים. הבוט שלח סיכום לערוץ הציבורי")

        if now.strftime("%H:%M") in ["19:40", "21:40", "22:40"]:
            fundamentals = analyze_fundamentals(STOCK_LIST)
            technicals = run_technical_analysis(STOCK_LIST)
            best_signal = "איתות סופי לדוגמה – עם כל הפרטים"  # Placeholder
            send_discord_message(DISCORD_PUBLIC_WEBHOOK_URL, best_signal)

    except Exception as e:
        send_discord_message(DISCORD_ERROR_WEBHOOK_URL, f"שגיאה בבוט: {str(e)}")
