# reporting.py

from report_generator import send_monthly_report_to_discord
from macro_analyzer import analyze_macro_trends
from trade_manager import analyze_open_trades
from datetime import datetime

def send_monthly_report_if_needed():
    if datetime.today().day == 1:
        print("שליחת דוח חודשי")
        send_monthly_full_report()

def send_weekly_report():
    # שליחת דוח שבועי בימי שבת בשעה 12:00 בצהריים
    print("שליחת דוח שבועי")

    send_weekly_full_report()

def send_weekly_full_report():
    analyze_macro_trends()
    analyze_open_trades()
    print("Weekly report sent successfully.")

def send_monthly_full_report():
    print("Generating full monthly report...")
    send_monthly_report_to_discord()
    print("Monthly report sent.")
