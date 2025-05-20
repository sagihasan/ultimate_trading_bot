# reporting.py

from report_generator import send_monthly_report_to_discord
from macro_analyzer import analyze_macro_trends
from trade_manager import analyze_open_trades
from discord_manager import send_private_message
from datetime import datetime

def send_monthly_report_if_needed():
    if datetime.today().day == 1:
        print("שליחה זה הדוח החודשי")
        send_monthly_full_report()

def send_weekly_report():
    # שליחת דוח שבועי ביום שבת בשעה 12:00 בצהריים
    print("שליחה זה דוח שבועי")
    send_weekly_full_report()

def send_weekly_full_report():
    macro = analyze_macro_trends()
    trades = analyze_open_trades()
    
    message = "**דוח שבועי - ניתוחים ועדכונים:**\n"
    message += f"{macro}\n\n"
    message += f"{trades}"
    
    send_private_message(message)
    print("Weekly report sent.")

def send_monthly_full_report():
    print("Generating full monthly report...")
    send_monthly_report_to_discord()
    print("Monthly report sent.")
