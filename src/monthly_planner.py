# monthly_planner.py

import os
from datetime import datetime
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
    tax_estimate = round(target_profit * 0.25, 2)
    after_tax_profit = round(target_profit - tax_estimate, 2)

    message = f"""
**תוכנית חודשית - {today.strftime('%B %Y')}**

• גודל תיק: ${account_size}
• יעד רווח לחודש: ${target_profit} ({monthly_target_pct}%)
• הערכת מיסוי: ${tax_estimate}
• רווח לאחר מיסוי: ${after_tax_profit}

מטרות חודשיות:
• כמות עסקאות מומלצת: 15–25
• דגש אסטרטגי:
  - כניסה באזורים אסטרטגיים (Demand Zone / Golden Zone)
  - איתור מניות בתמחור הוגן ב־Buffett Zone

• ניהול סיכונים: סיכון מבוקר לפי גודל תיק

הבוט מוכן לחודש חדש – בהצלחה!
"""

    send_private_message(message.strip())
