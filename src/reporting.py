# reporting.py

from report_generator import send_monthly_report_to_discord
from monthly_planner import send_monthly_plan
from macro_analyzer import analyze_macro_trends
from trade_manager import analyze_open_trades
from datetime import datetime

def send_monthly_report_if_needed():
    today = datetime.today()
    if today.day == 1:
        print(f"שליחת דוח חודשי – היום: {today.strftime('%Y-%m-%d')}")
        send_monthly_full_report()
    else:
        print(f"היום אינו תחילת החודש ({today.strftime('%Y-%m-%d')}) – לא נשלח דוח חודשי")

def send_weekly_report():
    today = datetime.today()
    if today.weekday() == 5:  # שבת
        print(f"שליחת דוח שבועי – היום: {today.strftime('%Y-%m-%d')}")
        send_weekly_full_report()
    else:
        print(f"היום אינו שבת ({today.strftime('%Y-%m-%d')}) – לא נשלח דוח שבועי")

def send_weekly_full_report():
    analyze_macro_trends()
    analyze_open_trades()
    print("Weekly report sent successfully.")

def send_monthly_full_report():
    print("Generating full monthly report...")
    send_monthly_report_to_discord()
    print("Monthly report sent.")
