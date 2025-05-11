# reporting.py – יצירת ושליחת דוחות שבועיים וחודשיים

import os
from datetime import datetime
from config import DISCORD_PRIVATE_WEBHOOK
from utils import save_to_excel, create_return_chart, create_pdf_report, send_discord_message, calculate_tax

# נתונים לדוגמה – בפועל יגיעו מקבצי מעקב עסקאות
sample_trades = [
    {"symbol": "AAPL", "date": "2024-05-12", "return": 4.5},
    {"symbol": "NVDA", "date": "2024-05-13", "return": 2.3},
    {"symbol": "PLTR", "date": "2024-05-14", "return": -1.2},
]

# שמות קבצים
EXCEL_FILE = "trades_log.xlsx"
PDF_FILE = "report.pdf"
CHART_FILE = "cumulative_return.png"

# שליחת דוח שבועי

def send_weekly_report():
    returns = [t["return"] for t in sample_trades]
    cumulative = [sum(returns[:i+1]) for i in range(len(returns))]

    save_to_excel(sample_trades, EXCEL_FILE)
    create_return_chart(cumulative, CHART_FILE)

    summary_text = "דוח שבועי – {}-{}\n".format("18/5", "23/5")
    summary_text += f"סה""כ תשואה: {round(sum(returns), 2)}%\n"
    summary_text += "עסקאות: {} | הצלחות: {} | כישלונות: {}\n".format(
        len(sample_trades), sum(1 for t in returns if t > 0), sum(1 for t in returns if t <= 0)
    )
    create_pdf_report(summary_text, PDF_FILE)

    send_discord_message(DISCORD_PRIVATE_WEBHOOK, "דוח שבועי נשלח. קבצים מצורפים:")

# שליחת דוח חודשי כולל חישוב מס

def send_monthly_report():
    returns = [t["return"] for t in sample_trades]
    total_return = sum(returns)
    total_profit = round(951 * (total_return / 100), 2)

    tax_result = calculate_tax(total_profit, tax_rate=0.25, tax_shield=0)

    save_to_excel(sample_trades, EXCEL_FILE)
    create_return_chart([sum(returns[:i+1]) for i in range(len(returns))], CHART_FILE)

    summary_text = "דו""ח חודשי – חודש מאי\n"
    summary_text += f"רווח חודשי: {total_profit}$ ({round(total_return, 2)}%)\n"
    summary_text += f"מס (25%): {round(tax_result['tax_due'], 2)}$\n"
    summary_text += f"רווח לאחר מס: {round(tax_result['net_profit'], 2)}$\n"

    create_pdf_report(summary_text, PDF_FILE)

    send_discord_message(DISCORD_PRIVATE_WEBHOOK, "דו""ח חודשי נשלח. קבצים מצורפים:")
