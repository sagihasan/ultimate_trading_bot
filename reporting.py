import pandas as pd
from utils import save_to_excel, create_return_chart, create_pdf_report, calculate_tax, send_discord_message
from config import DISCORD_PRIVATE_WEBHOOK
from datetime import datetime


def generate_weekly_report(trades, returns):
    date_range = get_week_range()
    summary_text = create_summary_text(trades, returns, date_range)
    chart_path = "cumulative_return.png"
    pdf_path = "weekly_report.pdf"
    excel_path = "signals_log.xlsx"

    create_return_chart(returns, filename=chart_path)
    create_pdf_report(summary_text, filename=pdf_path)
    save_to_excel(trades, filename=excel_path)

    send_discord_message(DISCORD_PRIVATE_WEBHOOK, f"דו"ח שבועי מוכן לתאריכים: {date_range}", message_type="weekly_report")


def generate_monthly_report(trades, returns):
    today = datetime.today()
    month_name = today.strftime("%B")
    summary_text = create_summary_text(trades, returns, f"חודש {month_name}")
    chart_path = "monthly_return.png"
    pdf_path = "monthly_report.pdf"
    excel_path = "monthly_signals_log.xlsx"

    create_return_chart(returns, filename=chart_path)
    create_pdf_report(summary_text, filename=pdf_path)
    save_to_excel(trades, filename=excel_path)

    send_discord_message(DISCORD_PRIVATE_WEBHOOK, f"דו"ח חודשי עבור {month_name} מוכן. ראה קבצים מצורפים.", message_type="monthly_report")


def get_week_range():
    today = datetime.today()
    start = today - pd.to_timedelta(today.weekday(), unit="D")
    end = start + pd.to_timedelta(6, unit="D")
    return f"{start.strftime('%d/%m')}–{end.strftime('%d/%m')}"


def create_summary_text(trades, returns, date_range):
    total_profit = sum([t.get("profit", 0) for t in trades])
    tax_data = calculate_tax(total_profit)
    win_count = sum(1 for t in trades if t.get("profit", 0) > 0)
    loss_count = len(trades) - win_count
    win_rate = (win_count / len(trades)) * 100 if trades else 0

    summary = f"דו"ח ({date_range})\n"
    summary += f"סה\"כ עסקאות: {len(trades)} | הצלחות: {win_count} | כישלונות: {loss_count} | אחוז הצלחה: {win_rate:.1f}%\n"
    summary += f"רווח כולל: {tax_data['total_profit']}$ | מס: {tax_data['tax_due']}$ | רווח נטו: {tax_data['net_profit']}$\n"
    return summary
