# התחלה של main.py המלא עם כל הפיצ'רים, כולל Machine Learning, ניהול עסקאות, מאקרו ודוחות

import os
import time
from datetime import datetime, timedelta
from macro import send_macro_summary
import pytz
import exchange_calendars as ec
from dotenv import load_dotenv
from config import (
    ACCOUNT_SIZE, RISK_PERCENTAGE, STOP_LOSS_PERCENT,
    TAKE_PROFIT_PERCENT, DISCORD_PUBLIC_WEBHOOK,
    DISCORD_PRIVATE_WEBHOOK, DISCORD_ERROR_WEBHOOK, STOCK_LIST
)
from fundamentals import analyze_fundamentals
from technicals import run_technical_analysis
from trade_manager import manage_open_trades
from reporting import send_weekly_report, send_monthly_report
from macro import handle_macro_events, send_macro_summary
from utils import send_discord_message

load_dotenv()

nyse = ec.get_calendar("XNYS")

def is_half_day(date):
    schedule = nyse.schedule.loc[date:date]
    if not schedule.empty:
        open_time = schedule.iloc[0]['market_open']
        close_time = schedule.iloc[0]['market_close']
        return (close_time - open_time).seconds < 6.5 * 3600
    return False

def is_dst_gap_period():
    today = datetime.now().date()
    dst_us = datetime(today.year, 3, 10)
    dst_il = datetime(today.year, 3, 29)
    return dst_il > today and dst_us <= today

def get_market_day():
    return nyse.valid_days(
        start_date=datetime.now().date() - timedelta(days=1),
        end_date=datetime.now().date()
    )[0].date()

def main():
    try:
        today = datetime.now(pytz.timezone("America/New_York")).date()
        market_day = get_market_day()

        if today != market_day:
            send_discord_message(DISCORD_PUBLIC_WEBHOOK, "אין מסחר היום לפי לוח השנה של NYSE.")
            return

        half_day = is_half_day(today)
        gap_period = is_dst_gap_period()

        if half_day:
            signal_time = "19:40"
        elif gap_period:
            signal_time = "21:40"
        else:
            signal_time = "22:40"

        now = datetime.now(pytz.timezone("Asia/Jerusalem")).strftime("%H:%M")
        if now == signal_time:
            fundamentals = analyze_fundamentals(STOCK_LIST)
            technicals = run_technical_analysis(STOCK_LIST)
            manage_open_trades(fundamentals, technicals)

        # דוחות יומיים / שבועיים / חודשיים
        if now == "11:00":
            send_discord_message(DISCORD_PRIVATE_WEBHOOK, "התחלתי")
        if now == "02:10":
            send_discord_message(DISCORD_PRIVATE_WEBHOOK, "סיימתי")
        if now == "11:00" and datetime.now().weekday() == 6:
            send_discord_message(DISCORD_PUBLIC_WEBHOOK, "שבוע חדש התחיל\nהבוט מוכן לפעולה.\nבהצלחה לכולנו.")
        if now == "12:00" and datetime.now().weekday() == 6:
            send_macro_summary()
        if now == "12:00" and datetime.now().day == 1:
            send_monthly_report()
        if now == "12:00" and datetime.now().weekday() == 5:
            send_weekly_report()

        # טיפול באירועי מאקרו (שעה לפני ואחרי)
        handle_macro_events()

    except Exception as e:
        send_discord_message(DISCORD_ERROR_WEBHOOK, f"שגיאה בבוט: {str(e)}")

if __name__ == "__main__":
    main()
