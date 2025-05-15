from report_generator import generate_weekly_report, generate_monthly_report
from datetime import datetime

def send_scheduled_reports():
    now = datetime.now()
    day = now.weekday()  # שבת = 5 או 6 תלוי בהגדרה שלך
    date = now.day

    # אם זה שבת – דו"ח שבועי
    if day == 5 or day == 6:
        print("מפעיל דו\"ח שבועי...")
        generate_weekly_report()

    # אם זה ה־1 בחודש – דו"ח חודשי
    if date == 1:
        print("מפעיל דו\"ח חודשי...")
        generate_monthly_report()
