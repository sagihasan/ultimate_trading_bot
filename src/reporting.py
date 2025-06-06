from datetime import datetime
from report_generator import send_monthly_report_to_discord
from macro_analyzer import analyze_macro_trends
from trade_manager import analyze_open_trades
from discord_manager import send_private_message
from pytz import timezone
import pandas as pd
from datetime import datetime
import os

def get_sector_support_text(sector_analysis):
    supporting_sectors = [s for s in sector_analysis if sector_analysis[s] == "תומך"]
    opposing_sectors = [s for s in sector_analysis if sector_analysis[s] == "נוגד"]

    if len(supporting_sectors) >= 5:
        return "🟢 רוב הסקטורים תומכים באיתותים השבועיים – שוק יציב להתקדמות."
    elif 2 <= len(supporting_sectors) < 5:
        return "🟡 חלק מהסקטורים תומכים, אך יש שונות – נדרשת זהירות וניהול סיכון."
    else:
        return "🔴 רוב הסקטורים אינם תומכים – המלצה להמתין או לפעול בזהירות."

def log_trade_signal(ticker,
                     signal_type,
                     entry_price,
                     stop_loss,
                     take_profit,
                     notes=""):
    log_file = "signals_log.xlsx"

    # צור קובץ אם לא קיים
    if not os.path.exists(log_file):
        df = pd.DataFrame(columns=[
            "תאריך", "מניה", "סוג איתות", "מחיר כניסה", "סטופ לוס",
            "טייק פרופיט", "הערות"
        ])
    else:
        df = pd.read_excel(log_file)

    # הוסף שורה חדשה
    new_row = {
        "תאריך": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "מניה": ticker,
        "סוג איתות": signal_type,
        "מחיר כניסה": entry_price,
        "סטופ לוס": stop_loss,
        "טייק פרופיט": take_profit,
        "הערות": notes
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # שמור לקובץ
    df.to_excel(log_file, index=False)


israel_tz = timezone("Asia/Jerusalem")
now = datetime.now(israel_tz)


def send_monthly_report_if_needed():
    if datetime.now(israel_tz).day == 1:
        print("שולח דוח חודשי")
        send_monthly_full_report()


def send_weekly_report_if_needed():
    now = datetime.now()
    # 5 = שבת לפי datetime.weekday(), 12:00
    if now.weekday() == 5 and now.hour == 12 and now.minute == 0:
        print("שולח דוח שבועי")
        send_weekly_full_report()


def send_weekly_full_report():
    macro = analyze_macro_trends()
    trades = analyze_open_trades()

    message = "**דו\"ח שבועי - סקירה כללית**\n\n"
    message += f"{macro}\n\n"
    message += f"{trades}"

    send_private_message(message)


def send_monthly_full_report():
    print("Generating full monthly report...")
    send_monthly_report_to_discord()
    print("Monthly report sent.")
