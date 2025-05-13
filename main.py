import os
import time
from datetime import datetime, timedelta
import pytz
import pandas as pd
import exchange_calendars as ec
from dotenv import load_dotenv
from utils import send_discord_message, already_sent_holiday_message, mark_holiday_message_sent
from fundamentals import analyze_fundamentals
from technicals import run_technical_analysis
from config import (
    ACCOUNT_SIZE, RISK_PERCENTAGE, STOP_LOSS_PERCENTAGE, TAKE_PROFIT_PERCENTAGE,
    DISCORD_PUBLIC_WEBHOOK, DISCORD_ERROR_WEBHOOK, DISCORD_PRIVATE_WEBHOOK,
    ALPHA_VANTAGE_API_KEY, NEWS_API_KEY
)
from macro import send_macro_summary

load_dotenv()

STOCK_LIST = [
 "AAPL", "MSFT", "NVDA", "GOOG", "AMZN", "META", "TSLA", "AMD", "ADBE", "AVGO",
    "NFLX", "INTC", "CRM", "ORCL", "QCOM", "CSCO", "SHOP", "SNOW", "PLTR", "UBER",
    "BABA", "TCEHY", "LRCX", "ASML", "MU", "TXN", "PANW", "SMCI", "SEDG", "ENPH",
    "ZM", "DOCU", "SQ", "PYPL", "COIN", "SOFI", "ROKU", "DDOG", "NET", "ZS",
    "CROX", "DKNG", "HOOD", "HIMS", "PERI", "APP", "AI", "SOUN", "ANET", "SNEX",
    "CRGY", "ARKK", "NU", "ACHC", "SMMT", "ZIM", "GRPN", "RKT", "EBAY", "CVNA",
    "XBI", "PZZA", "ALSN", "AR", "ASGN", "ASTS", "ADI", "TEAM", "FSLR", "RUN",
    "BLNK", "LCID", "RIVN", "NIO", "XPEV", "LI", "CHPT", "TTD", "TTWO", "ATVI",
    "EA", "INTUIT", "ABNB", "LYFT", "WBD", "WMT", "COST", "TGT", "LOW", "HD",
    "SBUX", "MCD", "PEP", "KO", "JNJ", "MRK", "PFE", "CVX", "XOM", "APA",
    "FANG", "OXY", "SLB", "HAL", "WFC", "BAC", "C", "JPM", "GS", "MS",
    "BX", "SCHW", "V", "MA", "AXP", "TROW", "BK", "AMP", "SPY", "QQQ",
    "DIA", "IWM", "XLK", "XLF", "XLE", "XLY", "XLV", "XLP"
]

def is_half_day(nyse_calendar, date):
    try:
        schedule = nyse_calendar.schedule.loc[date:date]
        if not schedule.empty:
            open_time = schedule.iloc[0]['market_open']
            close_time = schedule.iloc[0]['market_close']
            return (close_time - open_time).seconds < 23400  # פחות מ-6.5 שעות
    except Exception as e:
        print(f"שגיאה בזיהוי חצי יום מסחר: {e}")
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
    try:
        nyse = ec.get_calendar("XNYS")
        today = datetime.now(pytz.timezone("Asia/Jerusalem"))
        now = datetime.now(pytz.timezone("Asia/Jerusalem"))

        # יום שבת: שליחת סיכום בלבד
        if today.weekday() == 6 and now.strftime("%H:%M") == "12:00":
            send_discord_message(DISCORD_PUBLIC_WEBHOOK, "אין מסחר היום.")
            send_macro_summary()

        # בדיקת חגים
        sessions = nyse.sessions_in_range(today.date(), today.date())
        if sessions.empty:
            date_str = today.strftime("%Y-%m-%d")
            if not already_sent_holiday_message(date_str):
                holiday_name = get_today_holiday_name()
                message = f"אין מסחר היום: {holiday_name}"
                send_discord_message(DISCORD_PUBLIC_WEBHOOK, message)
                mark_holiday_message_sent(date_str)
            return

        half_day = is_half_day(nyse, today.date())
        is_dst_gap = (datetime(today.year, 3, 8) <= today <= datetime(today.year, 11, 1))

        if half_day:
            close_time = datetime.combine(today.date(), datetime.strptime("13:00", "%H:%M").time())
            signal_time = (close_time - timedelta(minutes=20)).strftime("%H:%M")
        elif is_dst_gap:
            signal_time = "21:40"
        else:
            signal_time = "22:40"

        print(f"הבוט מתוזמן לאיתות בשעה {signal_time}")

        while True:
            now_time = datetime.now(pytz.timezone("Asia/Jerusalem")).strftime("%H:%M")
            if now_time >= signal_time:
                fundamentals = analyze_fundamentals()
                technicals = run_technical_analysis(STOCK_LIST)

                best_stock = None
                highest_score = 0

                for stock in technicals:
                    symbol = stock["symbol"]
                    score = stock.get("score", 0)
                    fundamentals_data = fundamentals.get(symbol, {})

                    trend = fundamentals_data.get("trend", "")
                    sentiment = fundamentals_data.get("sentiment", "")
                    sector = fundamentals_data.get("sector", "")
                    market_cap = fundamentals_data.get("market_cap", "")
                    zone = fundamentals_data.get("zone", "")

                    if score > highest_score:
                        highest_score = score
                        best_stock = {
                            "symbol": symbol,
                            "score": score,
                            "price": stock["price"],
                            "stop_loss": stock["stop_loss"],
                            "take_profit": stock["take_profit"],
                            "position_size": stock["position_size"],
                            "sector": sector,
                            "trend": trend,
                            "sentiment": sentiment,
                            "zone": zone
                        }

                if best_stock:
                    zone_note = f"\nאזור: {best_stock['zone']}"
                    trend_note = f"מגמה: {best_stock['trend']}"
                    if best_stock["trend"] == "מגמת עלייה":
                        decision = "**להיכנס לעסקת לונג**"
                    elif best_stock["trend"] == "מגמת ירידה":
                        decision = "**להיכנס לעסקת שורט**"
                    else:
                        decision = "**אין מגמה ברורה – סיכון מוגבר**"

                    best_signal = (
                        f"**איתות סופי** — {best_stock['symbol']}\n"
                        f"סקטור: {best_stock['sector']}\n"
                        f"{trend_note}\n"
                        f"מחיר כניסה: {best_stock['price']}\n"
                        f"סטופ לוס: {best_stock['stop_loss']}\n"
                        f"טייק פרופיט: {best_stock['take_profit']}\n"
                        f"גודל פוזיציה מומלץ: {best_stock['position_size']}\n"
                        f"חוזק טכני כולל: {best_stock['score']}\n"
                        f"{decision}"
                    )
                else:
                    best_signal = "הבוט רץ — לא נמצאה מניה מתאימה היום"

                send_discord_message(DISCORD_PUBLIC_WEBHOOK, best_signal)
                break

            time.sleep(30)

    except Exception as e:
        send_discord_message(DISCORD_ERROR_WEBHOOK, f"שגיאה בבוט הראשי: {e}")

if __name__ == "__main__":
    main()
