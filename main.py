import os
import time
from datetime import datetime, timedelta
import pytz
import exchange_calendars as ec
from dotenv import load_dotenv
from utils import send_discord_message
from fundamentals import analyze_fundamentals
from technicals import run_technical_analysis
from config import ACCOUNT_SIZE, RISK_PERCENTAGE, STOP_LOSS_PERCENT, TAKE_PROFIT_PERCENT

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
    return nyse.valid_days(start_date=now - timedelta(days=1), end_date=now + timedelta(days=1)).date[-1]

def is_dst_gap_period():
    today = datetime.now().date()
    dst_us = datetime(datetime.now().year, 3, 10)  # בערך מרץ
    dst_il = datetime(datetime.now().year, 3, 29)  # בערך סוף מרץ
    return dst_il > dst_us and dst_us <= today <= dst_il

def main():
    try:
        nyse = ec.get_calendar("XNYS")
        today = datetime.now(pytz.timezone("America/New_York")).date()
        market_day = get_current_market_day(nyse)

        if today != market_day:
            send_discord_message(os.getenv("DISCORD_PUBLIC_WEBHOOK"), "אין מסחר היום לפי לוח השנה של NYSE.")
            return

        half_day = is_half_day(nyse, today)
        is_gap = is_dst_gap_period()

        # זיהוי שעת סיום מסחר לפי סוג היום
        if half_day:
            close_time = datetime.combine(today, datetime.strptime("13:00", "%H:%M").time())
            signal_time = (close_time - timedelta(minutes=20)).strftime("%H:%M")
        elif is_gap:
            signal_time = "21:40"
        else:
            signal_time = "22:40"

        print(f"הבוט מאזין לאיתות בשעה: {signal_time}")

        while True:
            now = datetime.now(pytz.timezone("Asia/Jerusalem")).strftime("%H:%M")
            if now == signal_time:
                fundamentals = analyze_fundamentals()
                technicals = run_technical_analysis()

                for result in technicals:
                    if result["trend_daily"] == result["trend_weekly"]:
                        trend = result["trend_daily"]
                        price = result["price"]
                        sl = price * (1 - STOP_LOSS_PERCENT) if trend == "מגמת עלייה" else price * (1 + STOP_LOSS_PERCENT)
                        tp = price * (1 + TAKE_PROFIT_PERCENT) if trend == "מגמת עלייה" else price * (1 - TAKE_PROFIT_PERCENT)
                        risk = ACCOUNT_SIZE * RISK_PERCENTAGE
                        qty = int(risk / abs(price - sl)) if price != sl else 0

                        msg = (
                            f"איתות חדש ({'לונג' if trend == 'מגמת עלייה' else 'שורט'}):\n"
                            f"מניה: {result['symbol']}\n"
                            f"מחיר כניסה: {price:.2f}\n"
                            f"סטופ לוס: {sl:.2f}\n"
                            f"טייק פרופיט: {tp:.2f}\n"
                            f"כמות מניות: {qty}\n\n"
                            f"מגמות:\n"
                            f"יומי: {'לונג' if result['trend_daily'] == 'מגמת עלייה' else 'שורט'}\n"
                            f"שבועי: {'לונג' if result['trend_weekly'] == 'מגמת עלייה' else 'שורט'}\n"
                            f"חודשי: {'לונג' if result['trend_monthly'] == 'מגמת עלייה' else 'שורט'}\n\n"
                            f"תחזית פונדומנטלית: {fundamentals['future_outlook']}"
                        )

                        if half_day:
                            msg += "\nהערה: יום מסחר מקוצר – נפח תנודתי, היזהר."
                        if is_gap:
                            msg += "\nהערה: תקופת פערי שעון בין ישראל לארה"ב."

                        send_discord_message(os.getenv("DISCORD_PUBLIC_WEBHOOK"), msg)
                        break
                else:
                    send_discord_message(os.getenv("DISCORD_PUBLIC_WEBHOOK"), "לא נשלח איתות – לא התקיימו התנאים ביומי ובשבועי.")

                break
            time.sleep(30)
    except Exception as e:
        send_discord_message(os.getenv("DISCORD_ERROR_WEBHOOK"), f"שגיאה בבוט: {str(e)}")

if __name__ == "__main__":
    main()
