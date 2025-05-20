import os
import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF
from pathlib import Path
from discord_manager import send_private_message
from datetime import datetime

DATA_PATH = Path("data")
TRADES_LOG = DATA_PATH / "trades_log.xlsx"
TRADE_MGMT_LOG = DATA_PATH / "trade_management_log.xlsx"
REPORT_PDF = DATA_PATH / "monthly_report.pdf"
CUMULATIVE_RETURN_IMG = DATA_PATH / "cumulative_return.png"

def generate_macro_calendar_report():
    print("מילוי דוח מאקרו...")
    print("כרגע זה פייסהולדר ונעדכן בהמשך בדוח")
    return

def generate_reports():
    print("Running weekly and monthly reports... (placeholder)")

def generate_cumulative_return_chart():
    if not TRADES_LOG.exists():
        return None

    df = pd.read_excel(TRADES_LOG)
    df["תשואה מצטברת"] = (df["תשואה (%)"] / 100).cumprod()
    plt.figure()
    df["תאריך"].plot(title="תשואה מצטברת לפי תאריך", grid=True)
    df["תשואה מצטברת"].plot()
    plt.savefig(CUMULATIVE_RETURN_IMG)
    return CUMULATIVE_RETURN_IMG

def create_pdf_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="דו\"ח חודשי אוטומטי", ln=True, align="C")

    if CUMULATIVE_RETURN_IMG.exists():
        pdf.image(str(CUMULATIVE_RETURN_IMG), x=10, y=30, w=180)
    pdf.output(str(REPORT_PDF))

def send_monthly_report_to_discord():
    generate_cumulative_return_chart()
    create_pdf_report()

    if REPORT_PDF.exists():
        with open(REPORT_PDF, "rb") as f:
            now = datetime.now().strftime("%d/%m/%Y")
            send_private_message(f"דו\"ח חודשי ל-{now} נשלח בהצלחה.")
    else:
        send_private_message("שגיאה: הקובץ של הדו\"ח לא נוצר.")
