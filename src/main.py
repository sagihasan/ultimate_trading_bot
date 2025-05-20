# src/main.py
import os
import time
import traceback
from datetime import datetime

from stock_list      import STOCK_LIST
from fundamentals    import analyze_fundamentals
from technicals      import analyze_technicals
from after_market    import check_after_market_alert      #  ❱  אפשרי להפעלה בלילה
from pre_market      import check_pre_market_alert        #  ❱  אפשרי להפעלה בבוקר
from macro_alerts    import check_macro_alerts
from ml_model        import calculate_ai_score

from trade_management import (
    create_trade_entry,
    log_trade_result,
    manage_open_trades,
)

from reporting       import send_weekly_report_if_needed, send_monthly_report_if_needed
from discord_manager import (
    send_public_message,
    send_private_message,
    send_error_message,
    create_signal_message,
)

# פונקציית עזר שמפחיתה את העומס על-Discord (מוגדרת ב-src/utils.py)
from utils import send_message_with_delay

# ברירת-מחדל 1.2 ש׳ – אפשר לאפס כ-ENV var אם תרצה
RATE_LIMIT_SECONDS = float(os.getenv("DISCORD_RATE_LIMIT_SECONDS", 1.2))


def run_bot() -> None:
    """לולאת הסריקה הראשית של הבוט."""
    now = datetime.now()
    today_str   = now.strftime("%Y-%m-%d")
    time_str    = now.strftime("%H:%M")

    try:
        # ---------- בדיקות מאקרו כלליות ----------
        check_macro_alerts()

        # ---------- סריקה לפי מניה ----------
        for symbol in STOCK_LIST:
            fundamentals = analyze_fundamentals(symbol)
            technicals   = analyze_technicals(symbol)
            ai_result    = calculate_ai_score(symbol)      # ⬅ קריאת המודל

            if fundamentals and technicals and ai_result:
                # בניית ההודעה בתבנית אחידה
                message = create_signal_message({
                    "ticker"           : symbol,
                    "trend"            : technicals["trend"],
                    "entry_type"       : "Market",
                    "entry_price"      : technicals["ema_9"],
                    "stop_loss"        : technicals["ema_20"],
                    "take_profit"      : technicals["bb_upper"],
                    "trend_sentiment"  : technicals["trend"],
                    "zones"            : technicals["zones"],
                    "risk_pct"         : 2,
                    "risk_dollars"     : 20,
                    "reward_pct"       : 4,
                    "reward_dollars"   : 40,
                    "ai_score"         : ai_result["ai_score"],
                    "confidence_score" : ai_result["confidence"],
                })

                # שליחה בפערי זמן קבועים כדי לא לקבל 429
                send_message_with_delay(
                    send_public_message,
                    message,
                    RATE_LIMIT_SECONDS
                )

        # ---------- ניהול פוזיציות פתוחות ----------
        manage_open_trades()

        # ---------- דוחות ----------
        send_weekly_report_if_needed()
        send_monthly_report_if_needed()

        # אפשר לשלוח הודעת סיום פרטית אם תרצה:
        # send_private_message(f"הבוט סיים את הפעולה - {today_str} {time_str}")

    except Exception as e:
        err_txt = traceback.format_exc()
        send_error_message(f"```\nשגיאה ב-main:\n{err_txt}\n```")


if __name__ == "__main__":
    run_bot()
