import os
import time
from datetime import datetime, timedelta
import pytz
import exchange_calendars as ec
import pandas_market_calendars as mcal
from dotenv import load_dotenv

from utils import send_discord_message, already_sent_holiday_message, mark_holiday_message_sent, get_today_holiday_name
from fundamentals import analyze_fundamentals
from technicals import run_technical_analysis
from config import (
    ACCOUNT_SIZE, RISK_PERCENTAGE, STOP_LOSS_PERCENT, TAKE_PROFIT_PERCENT,
    DISCORD_PUBLIC_WEBHOOK, DISCORD_ERROR_WEBHOOK, DISCORD_PRIVATE_WEBHOOK,
    STOCK_LIST, ALPHA_VANTAGE_API_KEY, NEWS_API_KEY
)
from macro import send_macro_summary

load_dotenv()

def is_half_day(nyse_calendar, date):
    schedule = nyse_calendar.schedule.loc[date:date]
    if not schedule.empty:
        open_time = schedule.iloc[0]['market_open']
        close_time = schedule.iloc[0]['market_close']
        return (close_time - open_time).seconds < 6.5 * 3600
    return False

def get_current_market_day(nyse):
    try:
        now = datetime.now(pytz.timezone("America/New_York")).date()
        valid_days = nyse.schedule.loc[:now]
        return valid_days.index[-1]
    except Exception as e:
        send_discord_message(DISCORD_ERROR_WEBHOOK, f"שגיאה בזיהוי יום מסחר תקין: {str(e)}", message_type="error")
        return None

def is_dst_gap_period():
    today = datetime.now().date()
    dst_us = datetime(datetime.now().year, 3, 10)
    dst_il = datetime(datetime.now().year, 3, 29)
    return dst_il > dst_us and dst_us <= today <= dst_il

def main():
    try:
        nyse = mcal.get_calendar("XNYS")
        today = datetime.now(pytz.timezone("America/New_York")).date()
        now = datetime.now(pytz.timezone("Asia/Jerusalem"))
        market_day = get_current_market_day(nyse)

        # התחלה ביום ראשון
        if today.weekday() == 6 and now.strftime("%H:%M") == "11:00":
            send_discord_message(DISCORD_PRIVATE_WEBHOOK, "התחלתי את השבוע. הבוט מוכן.", message_type="start")

        if today.weekday() == 6 and now.strftime("%H:%M") == "12:00":
            send_macro_summary()

        # אם היום לא יום מסחר – שלח הודעה פעם אחת בלבד
        if today != market_day:
            date_str = today.strftime("%Y-%m-%d")
            if not already_sent_holiday_message(date_str):
                holiday_name = get_today_holiday_name()
                message = "אין מסחר היום לפי לוח שנה של NYSE."
                if holiday_name:
                    message += f" חג: {holiday_name}."
                send_discord_message(DISCORD_PUBLIC_WEBHOOK, message, message_type="market")
                mark_holiday_message_sent(date_str)
            return

        # בדיקת חצי יום או פערי שעון
        if is_half_day(nyse, today):
            close_time = datetime.combine(today, datetime.strptime("13:00", "%H:%M").time())
            signal_time = (close_time - timedelta(minutes=20)).strftime("%H:%M")
        elif is_dst_gap_period():
            signal_time = "21:40"
        else:
            signal_time = "22:40"

        print(f"הבוט ממתין לאיתות בשעה: {signal_time}")

        while True:
            now_time = datetime.now(pytz.timezone("Asia/Jerusalem")).strftime("%H:%M")
            if now_time == signal_time:
                fundamentals = analyze_fundamentals(STOCK_LIST)
                technicals = run_technical_analysis(STOCK_LIST)
                best_signal = "איתות סופי לדוגמה..."  # כאן יתבצע חישוב האיתות החזק
                send_discord_message(DISCORD_PUBLIC_WEBHOOK, best_signal, message_type="signal_main")
                break
            time.sleep(30)

    except Exception as e:
        send_discord_message(DISCORD_ERROR_WEBHOOK, f"שגיאה בבוט: {str(e)}", message_type="error")

if __name__ == "__main__":
    main()
