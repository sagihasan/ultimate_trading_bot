import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime
import time

# זיכרון של שליחת הודעות לפי webhook + סוג הודעה
last_sent_times = {}
SENT_HOLIDAY_LOG = "sent_holiday_messages.log"


def already_sent_holiday_message(date_str):
    if not os.path.exists(SENT_HOLIDAY_LOG):
        return False
    with open(SENT_HOLIDAY_LOG, "r") as f:
        return date_str in f.read()


def mark_holiday_message_sent(date_str):
    with open(SENT_HOLIDAY_LOG, "a") as f:
        f.write(date_str + "\n")


def get_today_holiday_name():
    # תוכל להרחיב את הרשימה הזו לפי הצורך
    holidays = {
        "2025-01-01": "New Year's Day",
        "2025-01-20": "Martin Luther King Jr. Day",
        "2025-02-17": "Presidents' Day",
        "2025-04-18": "Good Friday",
        "2025-05-26": "Memorial Day",
        "2025-07-04": "Independence Day",
        "2025-09-01": "Labor Day",
        "2025-11-27": "Thanksgiving Day",
        "2025-12-25": "Christmas Day"
    }
    today_str = datetime.now().strftime("%Y-%m-%d")
    return holidays.get(today_str, None)


# שליחת הודעה לדיסקורד עם מניעת עומס

def send_discord_message(webhook_url, message, message_type="default"):
    try:
        key = f"{webhook_url}_{message_type}"
        now = time.time()

        # בודק אם עברו 15 שניות מאז השליחה האחרונה מאותו סוג
        if key in last_sent_times and now - last_sent_times[key] < 15:
            print(f"נמנעה שליחה ({message_type}) (429) כדי למנוע עומס.")
            return

        data = {"content": message}
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        last_sent_times[key] = now

    except Exception as e:
        print(f"שגיאה בשליחה לדיסקורד: {e}")


# שמירה בטוחה מחילוץ מקונן

def safe_get(d, *keys):
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return None
    return d


# שמירה לקובץ אקסל

def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)


# יצירת גרף תשואה מצטברת

def create_return_chart(returns, filename="cumulative_return.png"):
    plt.figure(figsize=(10, 5))
    plt.plot(returns, marker='o')
    plt.title("גרף תשואה מצטברת")
    plt.xlabel("תאריך")
    plt.ylabel("תשואה מצטברת (%)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


# יצירת דוח PDF

def create_pdf_report(summary_text, filename="report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in summary_text.split("\n"):
        pdf.cell(200, 10, txt=line, ln=True, align='L')
    pdf.output(filename)


# חישוב מס ורווח נטו

def calculate_tax(total_profit, tax_rate=0.25, tax_shield=0):
    tax_due = max((total_profit * tax_rate) - tax_shield, 0)
    net_profit = total_profit - tax_due
    return {
        "total_profit": total_profit,
        "tax_rate": tax_rate,
        "tax_shield": tax_shield,
        "tax_due": tax_due,
        "net_profit": net_profit
    }
