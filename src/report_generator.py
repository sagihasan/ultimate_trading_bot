import os
import pandas as pd
from fpdf import FPDF

TRADES_LOG = "data/trades_log.xlsx"
REPORT_PATH = "reports/monthly_report.pdf"


def create_pdf_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'src/DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)

    pdf.cell(0, 10, "📊 דוח חודשי - סיכום עסקאות", ln=True)

    rows_to_print = min(10, len(df))

    for idx, row in df.tail(rows_to_print).iterrows():
        line = f"{row['תוצאה']} | {row['מניה']} | {row['תשואה (%)']}%"
        pdf.cell(0, 10, line, ln=True)

    if not os.path.exists(TRADES_LOG):
        pdf.set_font('DejaVu', '', 12)
        pdf.cell(0, 10, "⚠️ לא נמצא קובץ trades_log.xlsx", ln=True)
    else:
        try:
            df = pd.read_excel(TRADES_LOG)
            if df.empty:
                pdf.set_font('DejaVu', '', 12)
                pdf.cell(0, 10, "⚠️ הקובץ ריק – אין עסקאות לדווח", ln=True)
            else:
                required_columns = {"תוצאה", "מניה", "תשואה (%)"}
                if not required_columns.issubset(set(df.columns)):
                    pdf.set_font('DejaVu', '', 12)
                    pdf.cell(0, 10, "⚠️ הקובץ חסר עמודות נדרשות", ln=True)
                else:
                    pdf.set_font('DejaVu', '', 11)
                    for idx, row in df.tail(10).iterrows():
                        line = f"{row['תוצאה']} | {row['מניה']} | {row['תשואה (%)']}%"
                        pdf.cell(0, 10, line, ln=True)
        except Exception as e:
            pdf.set_font('DejaVu', '', 12)
            pdf.cell(0, 10, f"שגיאה בקריאת הקובץ: {e}", ln=True)

    os.makedirs("reports", exist_ok=True)
    pdf.output(REPORT_PATH)


def send_monthly_report_to_discord():
    from discord_manager import send_file_to_discord
    try:
        create_pdf_report()
        send_file_to_discord(REPORT_PATH, "📄 דוח חודשי מצורף")
        print("Monthly report sent.")
    except Exception as e:
        print(f"שגיאה בשליחת דוח חודשי: {e}")
