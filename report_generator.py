# report_generator.py

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

TRADES_FILE = "data/trades_log.xlsx"
REPORT_IMAGE_PATH = "data/monthly_return_chart.png"

def generate_monthly_report():
    try:
        df = pd.read_excel(TRADES_FILE)
        df["תאריך"] = pd.to_datetime(df["תאריך"])
        df["תשואה"] = df["return_%"].astype(float)

        today = datetime.today()
        first_day_current = today.replace(day=1)
        last_day_prev = first_day_current - pd.Timedelta(days=1)
        first_day_prev = last_day_prev.replace(day=1)

        df_month = df[(df["תאריך"] >= first_day_prev) & (df["תאריך"] <= last_day_prev)]
        if df_month.empty:
            return "אין נתונים לחודש הקודם – לא נשלח דו״ח חודשי."

        trades_count = len(df_month)
        total_return = df_month["תשואה"].sum()
        month_name = first_day_prev.strftime("%B").upper()

        # יעד ותוכנית
        target = f"להשיג לפחות {round(min(10, total_return + 5), 1)}% תשואה עם 90% הצלחה"
        plan = [
            "עסקאות עם ניקוד AI ≥ 85 בלבד",
            "לסחור רק במגמה תואמת יומית ושבועית",
            "להעדיף אזורי ביקוש או Buffett Zone",
            "להפעיל ניהול עסקה אקטיבי ועדכון סטופים"
        ]

        # הודעה
        report = f"""**דו״ח חודשי – חודש {month_name}**
עסקאות שבוצעו: {trades_count}
תשואה חודשית: {round(total_return, 2)}%

**מטרת החודש – {month_name}:**
{target}

**תוכנית פעולה:**
- {plan[0]}
- {plan[1]}
- {plan[2]}
- {plan[3]}

הצלחה היא לא מקרה. זאת משמעת.
"""
        return report

    except Exception as e:
        return f"שגיאה בדו\"ח חודשי: {e}"
