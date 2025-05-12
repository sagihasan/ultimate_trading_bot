# utils.py – כלים כלליים לשליחת הודעות, גרפים, דוחות ועוד

import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime
import time
import json

# זיכרון לשליחת הודעות לפי סוג
last_sent_times = {}
HOLIDAY_LOG_FILE = "sent_holidays.json"

# שליחת הודעה לדיסקורד עם מניעת הצפה
def send_discord_message(webhook_url, message, message_type="default"):
    try:
        key = f"{webhook_url}_{message_type}"
        now = time.time()

        # אם נשלחה הודעה כזו ב־15 שניות האחרונות – לא שולחים שוב
        if key in last_sent_times and now - last_sent_times[key] < 15:
            print(f"הודעת {message_type} נמנעה (rate limit)")
            return

        data = {"content": message}
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        last_sent_times[key] = now

    except Exception as e:
        print(f"שגיאה בשליחה לדיסקורד: {e}")

# בדיקה אם כבר נשלחה הודעת חג בתאריך מסוים
def already_sent_holiday_message(date_str):
    if not os.path.exists(HOLIDAY_LOG_FILE):
        return False
    with open(HOLIDAY_LOG_FILE, "r") as f:
        sent = json.load(f)
    return sent.get(date_str, False)

# סימון שתאריך חג כבר נשלח
def mark_holiday_message_sent(date_str):
    if os.path.exists(HOLIDAY_LOG_FILE):
        with open(HOLIDAY_LOG_FILE, "r") as f:
            sent = json.load(f)
    else:
        sent = {}
    sent[date_str] = True
    with open(HOLIDAY_LOG_FILE, "w") as f:
        json.dump(sent, f)

# שליחה בטוחה בתוך מילון מקונן
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

# חישוב מס ורווח נקי
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

# טעינת עסקאות שבוצעו
def load_trade_data(filename="data/trades_log.xlsx"):
    try:
        return pd.read_excel(filename).to_dict(orient="records")
    except:
        return []

# טעינת עסקאות פתוחות (לניהול)
def load_open_trades(filename="data/trade_management_log.xlsx"):
    try:
        return pd.read_excel(filename).to_dict(orient="records")
    except:
        return []

