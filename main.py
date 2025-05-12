import os
import time
from datetime import datetime, timedelta
import pytz
import exchange_calendars as ec
from dotenv import load_dotenv

from utils import send_discord_message, already_sent_holiday_message, mark_holiday_message_sent
from fundamentals import analyze_fundamentals
from technicals import run_technical_analysis
from config import ACCOUNT_SIZE, RISK_PERCENTAGE, STOP_LOSS_PERCENT, TAKE_PROFIT_PERCENT, DISCORD_PUBLIC_WEBHOOK, DISCORD_ERROR_WEBHOOK, DISCORD_PRIVATE_WEBHOOK, ALPHA_VANTAGE_API_KEY, NEWS_API_KEY, STOCK_LIST
from macro import send_macro_summary

load_dotenv()
error_logged = False  # למניעת כפילות הודעות שגיאה

def is_half_day(nyse_calendar, date):
    schedule = nyse_calendar.schedule.loc[date:date]
    if not schedule.empty:
        open_time = schedule.iloc[0]['market_open']
        close_time = schedule.iloc[0]['market_close']
        return (close_time - open_time).seconds < 6.5 * 3600
    return False

def get_today_holiday_name():
    try:
        import pandas_market_calendars as mcal
        nyse = mcal.get_calendar('NYSE')
        today = datetime.now(pytz.timezone("America/New_York")).date()
        holidays = nyse.holidays().holidays
        for holiday in holidays:
            if holiday.date() == today:
                return nyse.name
    except Exception:
        return None
    return None

def main():
    global error_logged
    try:
        nyse = ec.get_calendar("XNYS")
        today = datetime.now(pytz.timezone("America/New_York")).date()
        now = datetime.now(pytz.timezone("Asia/Jerusalem"))

        # הודעת פתיחה ודוח מאקרו ביום ראשון
        if today.weekday() == 6 and now.strftime("%H:%M") == "11:00":
            send_discord_message(DISCORD_PRIVATE_WEBHOOK, "התחלתי את השבוע. הבוט מוכן.", message_type="start")

        if today.weekday() == 6 and now.strftime("%H:%M") == "12:00":
            send_macro_summary()

        try:
            sessions = nyse.sessions_in_range(start_date=today - timedelta(days=1), end_date=today + timedelta(days=1))
            valid_days = [session.date() for session in sessions]
            if today not in valid_days:
                date_str = today.strftime("%Y-%m-%d")
                if not already_sent_holiday_message(date_str):
                    holiday_name = get_today_holiday_name()
                    message = "אין מסחר היום לפי לוח שנה של NYSE."
                    if holiday_name:
                        message += f" חג: {holiday_name}."
                    send_discord_message(DISCORD_PUBLIC_WEBHOOK, message, message_type="market")
                    mark_holiday_message_sent(date_str)
                return
        except Exception as e:
            if not error_logged:
                send_discord_message(DISCORD_ERROR_WEBHOOK, f"שגיאה בזיהוי יום מסחר תקין: {str(e)}", message_type="error")
                error_logged = True
            return

        # קביעת שעת איתות
        half_day = is_half_day(nyse, today)
        is_dst_gap = (datetime(today.year, 3, 10) <= today <= datetime(today.year, 3, 29))

        if half_day:
            close_time = datetime.combine(today, datetime.strptime("13:00", "%H:%M").time())
            signal_time = (close_time - timedelta(minutes=20)).strftime("%H:%M")
        elif is_dst_gap:
            signal_time = "21:40"
        else:
            signal_time = "22:40"

        print(f"הבוט ממתין לאיתות בשעה: {signal_time}")

        while True:
            now_time = datetime.now(pytz.timezone("Asia/Jerusalem")).strftime("%H:%M")
            if now_time == signal_time:
                fundamentals = analyze_fundamentals(STOCK_LIST)
                technicals = run_technical_analysis(STOCK_LIST)
                best_signal = "איתות סופי לדוגמה..."  # כאן תגיע הלוגיקה שלך לבחירת המניה
                send_discord_message(DISCORD_PUBLIC_WEBHOOK, best_signal, message_type="signal_main")
                break
            time.sleep(30)

    except Exception as e:
        if not error_logged:
            send_discord_message(DISCORD_ERROR_WEBHOOK, f"שגיאה בבוט: {str(e)}", message_type="error")
            error_logged = True

def run_main():
    main()
