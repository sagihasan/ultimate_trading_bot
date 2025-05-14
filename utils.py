# utils.py

import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime
import time
import json
import pytz

# Webhook לשגיאות
from config import DISCORD_ERROR_WEBHOOK

HOLIDAY_LOG_FILE = "sent_holiday_log.txt"
last_sent_times = {}

# === שליחת הודעה לדיסקורד ===
def send_discord_message(webhook_url, message, message_type="default"):
    try:
        key = f"{webhook_url}_{message_type}"
        now = time.time()
        if key in last_sent_times and now - last_sent_times[key] < 15:
            print(f"הודעת {message_type} נמנעה (rate limit)")
            return
        data = {"content": message}
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        last_sent_times[key] = now
    except Exception as e:
        print(f"שגיאה בשליחה לדיסקורד: {e}")

# === לוג חגים ===
def already_sent_holiday_message(date_str):
    if not os.path.exists(HOLIDAY_LOG_FILE):
        return False
    with open(HOLIDAY_LOG_FILE, "r") as f:
        lines = f.read().splitlines()
    return date_str in lines

def mark_holiday_message_sent(date_str):
    with open(HOLIDAY_LOG_FILE, "a") as f:
        f.write(date_str + "\n")

# === אירועים כלכליים מדומים (לדוגמה) ===
def get_upcoming_events():
    # רשימה מדומה של אירועים
    return [
        {"title": "נאום פאוול", "time": "17:00", "impact": "גבוה"},
        {"title": "דו\"ח CPI", "time": "15:30", "impact": "בינוני"},
    ]

# === עזר ===
def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

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

def create_pdf_report(summary_text, filename="report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in summary_text.split("\n"):
        pdf.cell(200, 10, txt=line, ln=True, align='L')
    pdf.output(filename)

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

# טוען עסקאות פתוחות (אם יש לך קובץ json או אחר)
def load_trade_data():
    if os.path.exists("trade_log.json"):
        with open("trade_log.json", "r") as f:
            return json.load(f)
    return []

def load_open_trades():
    if os.path.exists("open_trades.json"):
        with open("open_trades.json", "r") as f:
            return json.load(f)
    return []

