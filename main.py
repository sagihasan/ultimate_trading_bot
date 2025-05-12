# main.py – קובץ ראשי של הבוט

import os
import time
from datetime import datetime, timedelta
import pytz
import exchange_calendars as ec
from dotenv import load_dotenv

from utils import send_discord_message
from fundamentals import analyze_fundamentals
from technicals import run_technical_analysis
from config import ACCOUNT_SIZE, RISK_PERCENTAGE, STOP_LOSS_PERCENT, TAKE_PROFIT_PERCENT, DISCORD_PUBLIC_WEBHOOK, DISCORD_ERROR_WEBHOOK, STOCK_LIST
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
    now = datetime.now(pytz.timezone("America/New_York")).date()
    return nyse.sessions_in_range(now - timedelta(days=1), now + timedelta(days=1))[-1].date()

def is_dst_gap_period():
    today = datetime.now().date()
    dst_us = datetime(datetime.now().year, 3, 10)
    dst_il = datetime(datetime.now().year, 3, 29)
    return dst_il > dst_us and dst_us <= today <= dst_il

def main():
    try:
        nyse = ec.get_calendar("XNYS")
        today = datetime.now(pytz.timezone("America/New_York")).date()
        now = datetime.now(pytz.timezone("Asia/Jerusalem"))
        market_day = get_current_market_day(nyse)

        if today.weekday() == 6 and now.strftime("%H:%M") == "11:00":
            send_discord_message(os.getenv("DISCORD_PRIVATE_WEBHOOK"), "התחלתי את השבוע. הבוט מוכן.", message_type="start")

        if today.weekday() == 6 and now.strftime("%H:%M") == "12:00":
            send_macro_summary()

        if today != market_day:
            send_discord_message(DISCORD_PUBLIC_WEBHOOK, "אין מסחר היום לפי לוח שנה של NYSE.", message_type="market")
            return

        half_day = is_half_day(nyse, today)
        is_gap = is_dst_gap_period()

        if half_day:
            close_time = datetime.combine(today, datetime.strptime("13:00", "%H:%M").time())
            signal_time = (close_time - timedelta(minutes=20)).strftime("%H:%M")
        elif is_gap:
            signal_time = "21:40"
        else:
            signal_time = "22:40"

        print(f"הבוט ממתין לאיתות בשעה: {signal_time}")

        while True:
            now_time = datetime.now(pytz.timezone("Asia/Jerusalem")).strftime("%H:%M")
            if now_time == signal_time:
                fundamentals = analyze_fundamentals(STOCK_LIST)
                technicals = run_technical_analysis(STOCK_LIST)
                best_signal = "איתות סופי לדוגמה..."  # כאן יהיה חישוב העסקה החזקה ביותר
                send_discord_message(DISCORD_PUBLIC_WEBHOOK, best_signal, message_type="signal_main")
                break
            time.sleep(30)

    except Exception as e:
        send_discord_message(DISCORD_ERROR_WEBHOOK, f"שגיאה בבוט: {str(e)}", message_type="error")

if __name__ == "__main__":
    main()
