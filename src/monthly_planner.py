# monthly_planner.py

from datetime import datetime
import os
from discord_manager import send_private_message

def send_monthly_plan():
    today = datetime.today()
    if today.day != 1:
        return

    try:
        account_size = float(os.getenv("ACCOUNT_SIZE", 1000))
        monthly_target_pct = float(os.getenv("MONTHLY_TARGET_PERCENTAGE", 5))
    except ValueError:
        account_size = 1000
        monthly_target_pct = 5

    target_profit = round(account_size * (monthly_target_pct / 100), 2)

    message = f"""
תוכנית חודשית – {today.strftime('%B %Y')}

● גודל תיק: ₪{account_size}
● יעד רווח לחודש: ₪{target_profit} ({monthly_target_pct}%)

● כמות עסקאות מוערכת: 18–25
● דגש אסטרטגי: זיהוי מניות באיזורים אסטרטגיים (Demand Zone / Golden Zone)
● רמת סיכון מומלצת: סיכון נמוך עד בינוני

הבוט מוכן לחודש חדש – בהצלחה!
"""
    send_private_message(message.strip())
