import time
from datetime import datetime
from reporting import generate_weekly_report, generate_monthly_report
from trade_manager import manage_trades
from utils import load_trade_data, load_open_trades  # נניח שיש פונקציות כאלה


def run_scheduler():
    while True:
        now = datetime.now()
        day = now.weekday()  # יום בשבוע (0=שני, 6=ראשון)
        hour = now.hour
        minute = now.minute

        # טען נתוני עסקאות ותשואות אמיתיים
        trades = load_trade_data()
        returns = [t.get("cumulative_return", 0) for t in trades]  # או לפי לוגיקתך
        open_trades = load_open_trades()

        # דוח שבועי – כל שבת ב־12:00
        if day == 5 and hour == 12 and minute == 0:
            generate_weekly_report(trades, returns)

        # דוח חודשי – כל 1 לחודש ב־12:00
        if now.day == 1 and hour == 12 and minute == 0:
            generate_monthly_report(trades, returns)

        # ניהול עסקאות – כל חצי שעה אם יש עסקאות פתוחות
        if hour in range(10, 23) and minute in [0, 30] and open_trades:
            manage_trades(open_trades)

        time.sleep(60)  # בדיקה כל דקה


if __name__ == "__main__":
    run_scheduler()
