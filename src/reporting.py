from datetime import datetime
from report_generator import send_monthly_report_to_discord
from macro_analyzer import analyze_macro_trends
from trade_manager import analyze_open_trades
from discord_manager import send_private_message

def send_monthly_report_if_needed():
    if datetime.today().day == 1:
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
