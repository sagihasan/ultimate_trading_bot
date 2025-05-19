# reporting.py

from report_generator import send_monthly_report_to_discord
from macro_analyzer import analyze_macro_trends
from trade_manager import analyze_open_trades
from monthly_planner import send_monthly_plan
from datetime import datetime

def send_monthly_report_if_needed():
    today = datetime.today()
    if today.day == 1:
        print(f"[דוח חודשי] {today.strftime('%Y-%m-%d')} – שליחת תוכנית ודוח חודשי")
        send_monthly_plan()
        send_monthly_full_report()
    else:
        print(f"[דוח חודשי] {today.strftime('%Y-%m-%d')} – לא נשלח (לא היום הראשון בחודש)")

def send_weekly_report():
    today = datetime.today()
    if today.weekday() == 5:  # שבת
        print(f"[דוח שבועי] {today.strftime('%Y-%m-%d')} – שליחה")
        send_weekly_full_report()
    else:
        print(f"[דוח שבועי] {today.strftime('%Y-%m-%d')} – לא נשלח (לא שבת)")

def send_weekly_full_report():
    analyze_macro_trends()
    analyze_open_trades()
    print("Weekly report sent successfully.")

def send_monthly_full_report():
    print("Generating full monthly report...")
    send_monthly_report_to_discord()
    print("Monthly report sent.")
