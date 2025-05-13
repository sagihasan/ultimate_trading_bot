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
    DISCORD_PUBLIC_WEBHOOK, DISCORD_ERROR_WEBHOOK
)
from macro import send_macro_summary

load_dotenv()

def is_half_day(nyse_calendar, date):
    try:
        schedule = nyse_calendar.schedule.loc[date.strftime('%Y-%m-%d')]
        if not schedule.empty:
            open_time = schedule.iloc[0]['market_open']
            close_time = schedule.iloc[0]['market_close']
            return (close_time - open_time).seconds < 6 * 3600
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
        today = datetime.now(pytz.timezone("America/New_York"))
        now = datetime.now(pytz.timezone("Asia/Jerusalem"))

        if today.weekday() == 6 and now.strftime("%H:%M") == "11:00":
            send_discord_message(DISCORD_PUBLIC_WEBHOOK, "בוקר טוב לוחמים. התחלתי.")
        if today.weekday() == 6 and now.strftime("%H:%M") == "02:00":
            send_macro_summary()

        try:
            sessions = nyse.sessions_in_range(today, today)
            if sessions.empty:
                date_str = today.strftime("%Y-%m-%d")
                if not already_sent_holiday_message(date_str):
                    holiday_name = get_today_holiday_name()
                    message = "אין מסחר היום לפי לוח שנה של NYSE."
                    if holiday_name:
                        message += f" חג: {holiday_name}"
                    send_discord_message(DISCORD_PUBLIC_WEBHOOK, message)
                    mark_holiday_message_sent(date_str)
                return
        except Exception as e:
            send_discord_message(DISCORD_ERROR_WEBHOOK, f"שגיאה בזיהוי יום מסחר תקין: {e}")
            return

        half_day = is_half_day(nyse, today)
        is_dst_gap = (datetime(today.year, 3, 10) <= today <= datetime(today.year, 11, 10))

        if half_day:
            close_time = datetime.combine(today.date(), datetime.strptime("13:00", "%H:%M").time())
            signal_time = (close_time - timedelta(minutes=20)).time().strftime("%H:%M")
        elif is_dst_gap:
            signal_time = "21:40"
        else:
            signal_time = "22:40"

        print(f"הבוט מתזמן לאיתות בשעה {signal_time}")

        while True:
            now_time = datetime.now(pytz.timezone("Asia/Jerusalem")).strftime("%H:%M")
            if now_time >= signal_time:
                fundamentals = analyze_fundamentals()
                technicals = run_technical_analysis()
                best_stock = None
                highest_score = 0

                for stock in technicals:
                    symbol = stock["symbol"]
                    score = stock.get("score", 0)
                    fundamentals_data = fundamentals.get(symbol, {})

                    trend = fundamentals_data.get("trend", "")
                    sentiment = fundamentals_data.get("sentiment", "")
                    sector = fundamentals_data.get("sector", "")
                    market_cap = fundamentals_data.get("market_cap", 0)
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
                    if best_stock["trend"] == "צמיחה":
                        decision = "**פקודה: להיכנס לעסקה**"
                    elif best_stock["trend"] == "צניחה":
                        decision = "**פקודה: עסקת שורט**"
                    else:
                        decision = "**פקודה: להמתין – אין מגמה חדה**"

                    best_signal = (
                        f"**איתות סופי – {best_stock['symbol']}**\n"
                        f"סקטור: {best_stock['sector']}\n"
                        f"{trend_note}\n"
                        f"מחיר כניסה: {best_stock['price']}\n"
                        f"סטופ לוס: {best_stock['stop_loss']}\n"
                        f"טייק פרופיט: {best_stock['take_profit']}\n"
                        f"דירוג פונדמנטלי כולל: {best_stock['score']}\n"
                        f"זיהוי טכני כולל: {best_stock['sentiment']}\n"
                        f"{decision}"
                    )
                else:
                    best_signal = "הבוט היום שקט – לא נמצאה מניה מתאימה."

                send_discord_message(DISCORD_PUBLIC_WEBHOOK, best_signal)
                break

            time.sleep(30)

    except Exception as e:
        send_discord_message(DISCORD_ERROR_WEBHOOK, f"שגיאה בבוט: {e}")

if __name__ == "__main__":
    main()                            "take_profit": stock["take_profit"],
                            "position_size": stock["position_size"],
                            "sector": sector,
                            "trend": trend,
                            "sentiment": sentiment,
                            "zone": zone
                        }

                if best_stock:
                    zone_note = f"\n*הזדמנות באזור חם: {best_stock['zone']}*" if best_stock['zone'] else ""
                    trend_note = f"פונדומנטלי: {best_stock['trend']} | סנטימנט: {best_stock['sentiment']}"

                    if best_stock["trend"] == "צמיחה" and best_stock["sentiment"] == "חיובי":
                        decision = "**הבוט קובע: להיכנס לעסקה.**"
                    elif best_stock["trend"] == "צניחה" or best_stock["sentiment"] == "שלילי":
                        decision = "**הבוט קובע: לא להיכנס. להתרחק.**"
                    else:
                        decision = "**הבוט קובע: לא להיכנס. סיכון מוגבר.**"

                    best_signal = (
                        f"**איתות סופי – {best_stock['symbol']}**\n"
                        f"סקטור: {best_stock['sector']}\n"
                        f"{trend_note}\n"
                        f"מחיר כניסה: {best_stock['price']}$\n"
                        f"סטופ לוס: {best_stock['stop_loss']}$ | טייק פרופיט: {best_stock['take_profit']}$\n"
                        f"גודל פוזיציה מומלץ: {best_stock['position_size']} מניות\n"
                        f"חוזק טכני כולל: {best_stock['score']} מתוך 5{zone_note}\n"
                        f"{decision}"
                    )
                else:
                    best_signal = "אין איתותים שעומדים בתנאים הסופיים של הבוט היום."

                # ---- סיום לוגיקת איתות ----
                send_discord_message(DISCORD_PUBLIC_WEBHOOK, best_signal, message_type="signal_main")
                break

            time.sleep(30)

    except Exception as e:
        send_discord_message(DISCORD_ERROR_WEBHOOK, f"שגיאה בבוט: {str(e)}", message_type="error")

if __name__ == "__main__":
    main()
