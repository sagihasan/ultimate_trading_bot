import time
from datetime import datetime
from reporting import generate_weekly_report, generate_monthly_report
from trade_manager import manage_trades
from utils import load_trade_data, load_open_trades

def run_scheduler():
    while True:
        now = datetime.now()
        day = now.weekday()
        hour = now.hour
        minute = now.minute

        trades = load_trade_data()
        returns = [t.get("cumulative_return", 0) for t in trades]
        open_trades = load_open_trades()

        if day == 5 and hour == 12 and minute == 0:
            generate_weekly_report(trades, returns)

        if now.day == 1 and hour == 12 and minute == 0:
            generate_monthly_report(trades, returns)

        if 10 <= hour <= 22 and minute in [0, 30] and open_trades:
            manage_trades(open_trades)

        time.sleep(60)

if __name__ == "__main__":
    run_scheduler()
