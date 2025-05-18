import os
import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF
from pathlib import Path
from discord_manager import send_discord_message
from datetime import datetime

DATA_PATH = Path("data")
TRADES_LOG = DATA_PATH / "trades_log.xlsx"
TRADE_MGMT_LOG = DATA_PATH / "trade_management_log.xlsx"
REPORT_PDF = DATA_PATH / "monthly_report.pdf"
CUMULATIVE_RETURN_IMG = DATA_PATH / "cumulative_return.png"

def generate_cumulative_return_chart():
    if not TRADES_LOG.exists():
        return None

    df = pd.read_excel(TRADES_LOG)
    df["תשואה מצטברת"] = (1 + df["תשואה (%)"] / 100).cumprod()
    plt.figure()
    df["תשואה מצטברת"].plot(title="תשואה מצטברת", grid=True)
    plt.xlabel("מספר עסקה")
    plt.ylabel("תשואה")
    plt.savefig(CUMULATIVE_RETURN_IMG)
    plt.close()
    return CUMULATIVE_RETURN_IMG

def generate_pdf_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="דו\"ח חודשי – בוט Ultimate", ln=True, align="C")

    if TRADES_LOG.exists():
        df = pd.read_excel(TRADES_LOG)
        total_return = round(df["תשואה (%)"].sum(), 2)
        win_rate = round((df["תוצאה"] == "הצלחה").sum() / len(df) * 100, 2)
        pdf.cell(200, 10, txt=f"תשואה כוללת: {total_return}%", ln=True)
        pdf.cell(200, 10, txt=f"אחוז הצלחה: {win_rate}%", ln=True)

    if CUMULATIVE_RETURN_IMG.exists():
        pdf.image(str(CUMULATIVE_RETURN_IMG), x=10, y=50, w=180)

    pdf.output(REPORT_PDF)
    return REPORT_PDF

def send_monthly_report_to_discord():
    chart_path = generate_cumulative_return_chart()
    pdf_path = generate_pdf_report()

    send_discord_message("דו\"ח חודשי – סיכום בוט Ultimate:", file=str(pdf_path), is_private=True)
    send_discord_message("גרף תשואה מצטברת:", file=str(chart_path), is_private=True)
    send_discord_message("קובץ אקסל: trades_log.xlsx", file=str(TRADES_LOG), is_private=True)
    send_discord_message("קובץ אקסל: trade_management_log.xlsx", file=str(TRADE_MGMT_LOG), is_private=True)
