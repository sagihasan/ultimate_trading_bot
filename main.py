import os
import time
from datetime import datetime, timedelta
import pytz
import pandas as pd
import exchange_calendars as ec
from dotenv import load_dotenv
from utils import send_discord_message
from fundamentals import analyze_fundamentals
from technicals import run_technical_analysis
from stock_list import STOCK_LIST
from config import (
    ACCOUNT_SIZE, RISK_PERCENTAGE, STOP_LOSS_PERCENTAGE, TAKE_PROFIT_PERCENTAGE,
    DISCORD_PUBLIC_WEBHOOK, DISCORD_PRIVATE_WEBHOOK, DISCORD_ERROR_WEBHOOK,
    ALPHA_VANTAGE_API_KEY, NEWS_API_KEY
)

load_dotenv()

def is_half_day():
    today = datetime.now(pytz.timezone('US/Eastern')).date()
    half_days = [
        datetime(today.year, 7, 3).date(),      # Day before Independence Day
        datetime(today.year, 11, 24).date(),    # Day after Thanksgiving (Black Friday)
        datetime(today.year, 12, 24).date(),    # Christmas Eve
    ]
    return today in half_days

def is_time_gap():
    israel_time = datetime.now(pytz.timezone("Asia/Jerusalem"))
    us_time = datetime.now(pytz.timezone("US/Eastern"))
    return israel_time.hour - us_time.hour != 7

def log(message):
    print(f"[LOG - {datetime.now().strftime('%H:%M:%S')}] {message}")

def main():
    log("הבוט התחיל לפעול ומחכה לשעה 22:40...")
    while True:
        now = datetime.now(pytz.timezone("Asia/Jerusalem"))
        
        # כל שעה עגולה
        if now.minute == 0:
            log("הבוט מחפש אירועים כלכליים...")

        # בדיקת פרי מרקט
        if now.hour == 17:
            log("הבוט בודק עכשיו את הפרי מרקט")

        # בדיקת אפטר מרקט
        if now.hour == 22:
            log("הבוט בודק את סיום המסחר ומתכונן למחר")

        # איתות לקראת סיום מסחר
        if is_half_day():
            if now.strftime('%H:%M') == "19:40":
                log("הבוט מתכונן לשליחת איתות בשוק מקוצר...")
        elif is_time_gap():
            if now.strftime('%H:%M') == "20:40":
                log("הבוט מתכונן לשליחת איתות בתקופת פערי שעון...")
        else:
            if now.strftime('%H:%M') == "21:40":
                log("הבוט מתכונן לשליחת איתות ביום מסחר רגיל...")

        time.sleep(60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        send_discord_message(DISCORD_ERROR_WEBHOOK, f"שגיאת מערכת: {str(e)}")
