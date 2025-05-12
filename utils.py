import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime
import time

last_sent_times = {}
error_counts = {}


def send_discord_message(webhook_url, message, message_type="info"):
    global last_sent_times, error_counts

    key = f"{webhook_url}_{message_type}"
    now = time.time()

    # הגבלת שליחות לשגיאות חוזרות
    if "error" in message_type:
        error_counts[key] = error_counts.get(key, 0) + 1
        if error_counts[key] > 3:
            print(f"שגיאה נחסמה – יותר מדי שליחות {message_type}")
            return

    # מניעת שליחה חוזרת בפרק זמן קצר
    if key in last_sent_times and now - last_sent_times[key] < 15:
        print(f"נמנעה שליחה ({message_type}) (429)")
        return

    try:
        data = {"content": message}
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        last_sent_times[key] = now
    except Exception as e:
        print(f"שגיאה בשליחה לדיסקורד: {e}")


# פונקציות נוספות בקובץ utils.py

def safe_get(d, *keys):
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return None
    return d

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

