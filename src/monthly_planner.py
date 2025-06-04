from datetime import datetime
from discord_manager import send_private_message
from pytz import timezone


def send_monthly_plan():
    israel_tz = timezone("Asia/Jerusalem")
    now = datetime.now(israel_tz)
    if now.day != 1:
        return

    try:
        # נתונים לצורך החישוב
        account_size = 1000  # תוכל לשנות בהתאם
        monthly_target_pct = 5  # יעד רווח חודשי באחוזים
        target_profit = round(account_size * (monthly_target_pct / 100))
        tax_estimate = round(target_profit * 0.25, 2)  # נניח מס 25%
        after_tax_profit = round(target_profit - tax_estimate, 2)

        # שליחת הודעה חכמה לדיסקורד
        message = (
            f"**דו\"ח יעד חודשי – {today.strftime('%B %Y')}**\n"
            f"• גודל תיק: ${account_size}\n"
            f"• יעד רווח חודשי: {monthly_target_pct}% = ${target_profit}\n"
            f"• הערכת מס: ${tax_estimate}\n"
            f"• רווח צפוי לאחר מס: ${after_tax_profit}")
        send_private_message(message)

    except Exception as e:
        send_private_message(f"שגיאה בחישוב יעד חודשי: {str(e)}")


if __name__ == "__main__":
    send_monthly_plan()
