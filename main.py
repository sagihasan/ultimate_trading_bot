import os
import time
from datetime import datetime, timedelta
import pytz
import exchange_calendars as ec
from dotenv import load_dotenv
from utils import get_today_events
from utils import (
    send_discord_message,
    already_sent_holiday_message,
    mark_holiday_message_sent,
    get_upcoming_events,
    get_today_events,
    get_stock_list
)
from fundamentals import analyze_fundamentals
from technicals import run_technical_analysis
from macro import send_macro_summary

from config import (
    ACCOUNT_SIZE, RISK_PERCENTAGE, STOP_LOSS_PERCENTAGE, TAKE_PROFIT_PERCENTAGE,
    DISCORD_PUBLIC_WEBHOOK, DISCORD_ERROR_WEBHOOK, DISCORD_PRIVATE_WEBHOOK,
    ALPHA_VANTAGE_API_KEY, NEWS_API_KEY
)

load_dotenv()

STOCK_LIST = get_stock_list()

def is_half_day(nyse_calendar, date):
    schedule = nyse_calendar.schedule.loc[date:date]
    if not schedule.empty:
        open_time = schedule.iloc[0]['market_open']
        close_time = schedule.iloc[0]['market_close']
        return (close_time - open_time).seconds < 6.5 * 3600
    return False

def main():
    try:
        nyse = ec.get_calendar("XNYS")
        today = datetime.now(pytz.timezone("America/New_York")).date()
        now = datetime.now(pytz.timezone("Asia/Jerusalem"))

        weekday = today.weekday()

        print("הבוט התעורר בשעה 09:30, יתחיל לפעול ב־11:00")

        if now.strftime("%H:%M") == "11:00":
            send_discord_message(DISCORD_PRIVATE_WEBHOOK, "הבוט התחיל לפעול. בדוק בערוץ הפרטי.", message_type="log")

        if now.strftime("%H:%M") == "11:10":
            print("הבוט התחיל לבדוק את הפרי־מרקט")

        if weekday == 6 and now.strftime("%H:%M") == "12:00":
            send_macro_summary()
            print("הבוט שלח עדכון מאקרו")

        # בדיקת יום מסחר
        sessions = nyse.sessions_in_range(start_date=now - timedelta(days=1), end_date=now + timedelta(days=1))
        if today not in sessions:
            date_str = today.strftime("%Y-%m-%d")
            if not already_sent_holiday_message(date_str):
                send_discord_message(DISCORD_PUBLIC_WEBHOOK, "אין מסחר היום לפי לוח שנה של NYSE.", message_type="market")
                mark_holiday_message_sent(date_str)
            return

        # הגדרת שעות לפי סוג היום
        is_gap = (datetime(today.year, 3, 10) <= today <= datetime(today.year, 3, 29))
        half_day = is_half_day(nyse, today)

        if half_day:
            print("הבוט סיים לבדוק את הפרי־מרקט והתחיל את המסחר. ישלח איתות 20 דקות לפני סגירה")
            signal_time = "19:40"  # לדוגמה
            end_message_time = "20:10"
        elif is_gap:
            print("הבוט סיים לבדוק את הפרי־מרקט והתחיל את המסחר. ישלח איתות ב־21:40 בגלל פערי שעון")
            signal_time = "21:40"
            end_message_time = "22:10"
        else:
            print("הבוט סיים לבדוק את הפרי־מרקט והתחיל את המסחר. ישלח איתות ב־22:40")
            signal_time = "22:40"
            end_message_time = "23:10"

        while True:
            now = datetime.now(pytz.timezone("Asia/Jerusalem"))
            now_str = now.strftime("%H:%M")

            # כל שעה עגולה – בדיקת אירועים כלכליים
            if now.minute == 0:
                print("הבוט מחפש אירועים כלכליים...")
                events = get_upcoming_events()
                for event in events:
                    event_time = event.get("time")
                    if event_time:
                        event_dt = datetime.strptime(event_time, "%H:%M") - timedelta(hours=1)
                        if now.strftime("%H:%M") == event_dt.strftime("%H:%M"):
                            send_discord_message(DISCORD_PUBLIC_WEBHOOK, f"זוהה אירוע כלכלי: {event.get('title')}. הבוט קובע: {'היכנס' if 'positive' in event.get('impact', '') else 'אל תיכנס'}.", message_type="macro")

                # שליחת סיכום לאחר האירוע
                for event in get_today_events():
                    event_time = event.get("time")
                    if event_time:
                        event_dt = datetime.strptime(event_time, "%H:%M") + timedelta(minutes=15)
                        if now.strftime("%H:%M") == event_dt.strftime("%H:%M"):
                            send_discord_message(DISCORD_PUBLIC_WEBHOOK, f"האירוע '{event.get('title')}' הסתיים. הבוט שלח את הסיכום לערוץ הציבורי.", message_type="macro")

            # שליחת איתות יומי
            if now_str == signal_time:
                fundamentals = analyze_fundamentals(STOCK_LIST)
                technicals = run_technical_analysis(STOCK_LIST)
                best_signal = "איתות סופי לדוגמה..."
                send_discord_message(DISCORD_PUBLIC_WEBHOOK, best_signal, message_type="signal_main")

            # שליחת הודעת סיום
            if now_str == "02:00":
                send_discord_message(DISCORD_PRIVATE_WEBHOOK, "הבוט סיים לפעול. נשלחה הודעת עדכון יומי.", message_type="end")
                break

            time.sleep(30)

    except Exception as e:
        send_discord_message(DISCORD_ERROR_WEBHOOK, f"שגיאה בבוט: {str(e)}", message_type="error")

if __name__ == "__main__":
    main()
