# run_bot.py

from analysis import analyze_all_stocks
from discord_manager import send_signal_message
from reporting import log_trade_signal
from fundamentals import analyze_fundamentals
from trade_management import manage_open_trades
from macro import get_macro_summary
from alerts import check_macro_events
from messaging import send_error_message


def run_bot():
    try:
        print("📈 הבוט התחיל להריץ ניתוחים...")

        # ניתוח מאקרו
        macro_summary = get_macro_summary()
        check_macro_events(macro_summary)  # התראה על אירועים צפויים

        # ניתוח פונדומנטלי וניתוחים טכניים לכל המניות
        signals = analyze_all_stocks()

        # ניהול עסקאות פתוחות (עדכון סטופים, טייקים וכו')
        manage_open_trades()

        # שליחת איתותים במידת הצורך
        for signal in signals:
            send_signal_message(signal)
            log_trade_signal(signal)

        print("✅ הבוט סיים את הניתוחים והאיתותים")

    except Exception as e:
        error_message = f"שגיאה בבוט הראשי: {e}"
        print(error_message)
        send_error_message(error_message)
