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

        # גרף תשואה מצטברת
        df["תשואה מצטברת"] = df["תשואה"].cumsum()
        plt.figure(figsize=(10, 5))
        plt.plot(df["תאריך"], df["תשואה מצטברת"], marker='o')
        plt.title("גרף תשואה מצטברת – בוט קרבי")
        plt.xlabel("תאריך")
        plt.ylabel("תשואה מצטברת (%)")
        plt.grid(True)
        plt.tight_layout()
        chart_path = "data/weekly_return_chart.png"
        plt.savefig(chart_path)
        plt.close()

        # שליחת הודעה לדיסקורד עם סיכום
        last_week = df[df["תאריך"] >= df["תאריך"].max() - pd.Timedelta(days=7)]
        trades_count = len(last_week)
        total_return = last_week["תשואה"].sum()

        summary = f"""**דו״ח שבועי – בוט קרבי**
עסקאות שבוצעו השבוע: {trades_count}
תשואה כוללת: {round(total_return, 2)}%
הגרף צורף למטה.
"""

        send_discord_message(summary)
        send_discord_message("מצורף גרף תשואה:", is_private=True)
        with open(chart_path, 'rb') as f:
            send_discord_message(file=f)

    except Exception as e:
        send_discord_message(f"שגיאה ביצירת הדו\"ח השבועי: {e}")
