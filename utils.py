import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime
import time
import json

last_sent_times = {}

# שליחת הודעה לדיסקורד עם מניעת ספאם
def send_discord_message(webhook_url, message, message_type="default"):
    try:
        key = f"{webhook_url}_{message_type}"
        now = time.time()
        if key in last_sent_times and now - last_sent_times[key] < 60:
            print(f"נמנעה שליחה ({message_type}) בגלל תזמון.")
            return
        data = {"content": message}
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        last_sent_times[key] = now
    except Exception as e:
        print(f"שגיאה בשליחה לדיסקורד: {e}")

# שליחה בטוחה מקוננים
def safe_get(d, *keys):
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return None
    return d

# שמירה לאקסל
def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

# טעינת עסקאות קודמות מדוח
def load_trade_data():
    try:
        return pd.read_excel("signals_log.xlsx").to_dict(orient="records")
    except:
        return []

# טעינת עסקאות פתוחות
def load_open_trades():
    try:
        return pd.read_excel("open_trades.xlsx").to_dict(orient="records")
    except:
        return []

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

# ניהול הודעות חג – שמירה לקובץ JSON
HOLIDAY_LOG = "holiday_log.json"

def already_sent_holiday_message(date_str):
    if not os.path.exists(HOLIDAY_LOG):
        return False
    with open(HOLIDAY_LOG, "r") as f:
        data = json.load(f)
    return data.get(date_str, False)

def mark_holiday_message_sent(date_str):
    if os.path.exists(HOLIDAY_LOG):
        with open(HOLIDAY_LOG, "r") as f:
            data = json.load(f)
    else:
        data = {}
    data[date_str] = True
    with open(HOLIDAY_LOG, "w") as f:
        json.dump(data, f)

# זיהוי שם חג היום לפי תאריך ידוע
HOLIDAYS = {
    "2025-01-01": "ראש השנה האזרחית",
    "2025-01-20": "Martin Luther King Jr. Day",
    "2025-02-17": "Presidents' Day",
    "2025-04-18": "Good Friday",
    "2025-05-26": "Memorial Day",
    "2025-07-04": "Independence Day",
    "2025-09-01": "Labor Day",
    "2025-11-27": "Thanksgiving",
    "2025-12-25": "Christmas"
}

def get_today_holiday_name():
    today_str = datetime.now().strftime("%Y-%m-%d")
    return HOLIDAYS.get(today_str)
