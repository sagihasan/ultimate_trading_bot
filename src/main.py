import os
import time
import traceback
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from stock_list import STOCK_LIST
from fundamentals import analyze_fundamentals
from technicals import analyze_technicals
from after_market import check_after_market_alert
from pre_market import check_pre_market_alert
from macro_alerts import check_macro_alerts
from ml_model import calculate_ai_score
from trade_management import (
    create_trade_entry,
    log_trade_result,
    manage_open_trades
)
from price_utils import get_current_price
from reporting import send_weekly_report_if_needed, send_monthly_report_if_needed
from discord_manager import (
    send_private_message,
    send_error_message,
    send_trade_update_message,
    DISCORD_PRIVATE_WEBHOOK,
    DISCORD_ERROR_WEBHOOK
)
from messaging import send_message, DISCORD_PUBLIC_WEBHOOK
from utils import (
    send_message_with_delay,
    get_current_time,
    get_current_time_str,
    format_time,
    is_weekend,
    is_market_open,
    current_date,
    short_date,
    log
)
def run_bot():
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M")

    try:
        send_private_message(f"הבוט התחיל לפעול - {today} {current_time}")

        if current_time == "11:00":
            check_macro_alerts()

        check_macro_alerts()

        for symbol in STOCK_LIST:
            fundamentals = analyze_fundamentals(symbol)
            technicals = analyze_technicals(symbol)
            ai_result = calculate_ai_score(symbol)

            if fundamentals and technicals and ai_result:
                message = create_trade_entry(
                    symbol=symbol,
                    direction=technicals["trend"],
                    entry_price=technicals["ema_9"],
                    stop_loss=technicals["ema_20"],
                    take_profit=technicals["bb_upper"],
                    reason="AI + טכני + פונדומנטלי",
                    market_rating=technicals["trend"],
                    zone=technicals["zones"]
                )
                message_text = (
                    f"איתות עסקה:\n"
                    f"מניה: {symbol}\n"
                    f"מגמה: {technicals['trend']}\n"
                    f"כניסה: Market\n"
                    f"מחיר כניסה: {technicals['ema_9']}\n"
                    f"סטופ לוס: {technicals['ema_20']}\n"
                    f"טייק פרופיט: {technicals['bb_upper']}\n"
                    f"סנטימנט מגמה: {technicals['trend']}\n"
                    f"אזור טכני: {technicals['zones']}\n"
                    f"סיכון: 2%\n"
                    f"רווח צפוי: 4%\n"
                    f"ניקוד AI: {ai_result['ai_score']}\n"
                    f"רמת ביטחון: {ai_result['confidence']}"
                )
                send_message_with_delay(send_public_message, message)

        manage_open_trades()
        send_weekly_report_if_needed()
        send_monthly_report_if_needed()
        send_private_message(f"הבוט סיים את הפעולה - {today} {current_time}")

    except Exception as e:
        error = traceback.format_exc()
        message = f"שגיאה בבוט main:\n{error}"
        send_error_message(message)

if __name__ == "__main__":
    run_bot()
