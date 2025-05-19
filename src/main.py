import os
import time
from datetime import datetime
from config import STOCK_LIST
from fundamentals import analyze_fundamentals
from technicals import analyze_technicals
from ml_model import evaluate_trade_ai
from trade_management import manage_open_trades
from reporting import send_weekly_report_if_needed, send_monthly_report_if_needed
from macro_alerts import check_macro_alerts
from pre_market import check_pre_market_alert
from discord_manager import send_public_message, send_error_message, create_signal_message
import traceback

def run_bot():
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M")

    try:
        # שליחת הודעת התחלה (פרטי)
        from discord_manager import send_private_message
        send_private_message(f"הבוט התחיל לפעול - {today} {current_time}")

        # בדיקת פרה-מרקט בשעה 11:00 בבוקר בלבד
        if now.hour == 11 and now.minute < 10:
            for symbol in STOCK_LIST:
                check_pre_market_alert(symbol)

        # בדיקת מקרו כל שעה
        check_macro_alerts()

        # ניתוחים ואיתותים (יומי)
        for symbol in STOCK_LIST:
            fundamentals = analyze_fundamentals(symbol)
            technicals = analyze_technicals(symbol)
            ai_result = evaluate_trade_ai(symbol)

            if fundamentals and technicals and ai_result:
                message = create_signal_message(
                    ticker=symbol,
                    direction=technicals["trend"],
                    order_type="Market",
                    entry_price=technicals["ema_9"],
                    stop_loss=technicals["ema_20"],
                    take_profit=technicals["bb_upper"],
                    trend_sentiment=technicals["trend"],
                    zones=technicals["zones"],
                    risk_pct=2,
                    risk_dollars=20,
                    reward_pct=4,
                    reward_dollars=40,
                    ai_score=ai_result["ai_score"],
                    confidence_score=ai_result["confidence"]
                )
                send_public_message(message)

        # ניהול עסקאות פתוחות
        manage_open_trades()

        # דוחות
        send_weekly_report_if_needed()
        send_monthly_report_if_needed()

        # שליחת הודעת סיום (פרטי)
        send_private_message(f"הבוט סיים את הפעולה - {today} {current_time}")

    except Exception as e:
        error = traceback.format_exc()
        send_error_message(f"שגיאה ב-main: {e}
```{error}```")

if __name__ == "__main__":
    run_bot()
