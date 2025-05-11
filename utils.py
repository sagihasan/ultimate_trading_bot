# utils.py – שליחת הודעות, שמירת דוחות, גרפים, PDF, חישובי מס ומגן מס

import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime

# שליחת הודעה לדיסקורד

def send_discord_message(webhook_url, message):
    try:
        payload = {"content": message}
        requests.post(webhook_url, json=payload)
    except Exception as e:
        print(f"שגיאה בשליחת הודעה לדיסקורד: {e}")

# שמירת קובץ אקסל לאיתותים / דוחות

def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

# יצירת גרף תשואה מצטברת ושמירתו

def create_return_chart(returns, filename="cumulative_return.png"):
    plt.figure(figsize=(10, 5))
    plt.plot(returns, marker='o')
    plt.title("גרף תשואה מצטברת")
    plt.xlabel("עסקאות")
    plt.ylabel("תשואה מצטברת (%)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

# יצירת קובץ PDF סיכום

def create_pdf_report(summary_text, filename="report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in summary_text.split("\n"):
        pdf.cell(200, 10, txt=line, ln=True, align='L')
    pdf.output(filename)

# חישוב מס ומגן מס

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
