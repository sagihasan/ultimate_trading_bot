import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from discord_manager import send_discord_message

TRADES_FILE = "data/trades_log.xlsx"
MANAGEMENT_FILE = "data/trade_management_log.xlsx"

def generate_weekly_report():
    try:
        df = pd.read_excel(TRADES_FILE)
        df["תאריך"] = pd.to_datetime(df["תאריך"])
        df["תשואה"] = df["תוצאה"].astype(float)

        end_date = df["תאריך"].max()
        start_date = end_date - pd.Timedelta(days=6)
        df_week = df[(df["תאריך"] >= start_date) & (df["תאריך"] <= end_date)]

        if df_week.empty:
            send_discord_message("אין נתונים לשבוע האחרון – לא נשלח דו\"ח שבועי.")
            return

        df_week["תשואה מצטברת"] = df_week["תשואה"].cumsum()
        plt.figure(figsize=(10, 5))
        plt.plot(df_week["תאריך"], df_week["תשואה מצטברת"], marker='o')
        plt.title("גרף תשואה שבועי")
        plt.xlabel("תאריך")
        plt.ylabel("תשואה מצטברת (%)")
        plt.grid(True)
        plt.tight_layout()
        chart_path = "data/weekly_return_chart.png"
        plt.savefig(chart_path)
        plt.close()

        trades_count = len(df_week)
        total_return = df_week["תשואה"].sum()
        date_range = f"{start_date.strftime('%d/%m')} – {end_date.strftime('%d/%m')}"

        summary = f"""**דו״ח שבועי – טווח {date_range}**
עסקאות שבוצעו: {trades_count}
תשואה שבועית כוללת: {round(total_return, 2)}%
"""

        send_discord_message(summary)
        with open(chart_path, 'rb') as f:
            send_discord_message("גרף תשואה שבועי:", is_private=True)
            send_discord_message(file=f)

    except Exception as e:
        send_discord_message(f"שגיאה בדו\"ח שבועי: {e}", is_private=True)

def generate_monthly_report():
    try:
        df = pd.read_excel(TRADES_FILE)
        df["תאריך"] = pd.to_datetime(df["תאריך"])
        df["תשואה"] = df["תוצאה"].astype(float)

        # טווח החודש הקודם
        today = datetime.today()
        first_day_current = today.replace(day=1)
        last_day_prev = first_day_current - pd.Timedelta(days=1)
        first_day_prev = last_day_prev.replace(day=1)

        df_month = df[(df["תאריך"] >= first_day_prev) & (df["תאריך"] <= last_day_prev)]
        if df_month.empty:
            send_discord_message("אין נתונים לחודש הקודם – לא נשלח דו״ח חודשי.", is_private=True)
            return

        trades_count = len(df_month)
        total_return = df_month["תשואה"].sum()
        month_name = first_day_prev.strftime("%B").upper()  # MAY לדוגמה

        # גרף
        df_month["תשואה מצטברת"] = df_month["תשואה"].cumsum()
        plt.figure(figsize=(10, 5))
        plt.plot(df_month["תאריך"], df_month["תשואה מצטברת"], marker='o')
        plt.title(f"גרף תשואה חודשי – חודש {month_name}")
        plt.xlabel("תאריך")
        plt.ylabel("תשואה מצטברת (%)")
        plt.grid(True)
        plt.tight_layout()
        chart_path = "data/monthly_return_chart.png"
        plt.savefig(chart_path)
        plt.close()

        # מיסוי
        taxable_profit = total_return if total_return > 0 else 0
        expected_tax = round(taxable_profit * 0.25, 2)
        loss_shield = abs(df_month[df_month["תשואה"] < 0]["תשואה"].sum())
        net_profit = round(total_return - expected_tax, 2) if total_return > 0 else total_return

        summary = f"""**דו״ח חודשי – חודש {month_name}**
עסקאות שבוצעו: {trades_count}
תשואה חודשית: {round(total_return, 2)}%
מס צפוי: {expected_tax}%
מגן מס: {round(loss_shield, 2)}%
רווח נטו לאחר מס: {net_profit}%
"""

        send_discord_message(summary, is_private=True)
        with open(chart_path, 'rb') as f:
            send_discord_message("גרף תשואה חודשי:", is_private=True)
            send_discord_message(file=f)

    except Exception as e:
        send_discord_message(f"שגיאה בדו\"ח חודשי: {e}", is_private=True)
