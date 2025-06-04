
from datetime import datetime
from pytz import timezone

def is_short_trading_day(today):
    # Example: add real holidays or half-day list from API or static list
    short_days = ['2025-07-03', '2025-11-28', '2025-12-24']
    return today.strftime('%Y-%m-%d') in short_days

def get_market_close_hour(today):
    # Return the close hour depending on regular / short day / timezone gap
    israel_tz = timezone("Asia/Jerusalem")
    now = datetime.now(israel_tz)

    # Example range for DST gap (real check should use pytz/zoneinfo calendar)
    tz_gap_dates = [
        ('2025-03-10', '2025-04-07'),
        ('2025-10-27', '2025-11-10')
    ]
    for start, end in tz_gap_dates:
        if start <= today.strftime('%Y-%m-%d') <= end:
            return 21  # Timezone gap period: market close at 21:30, send at 21:40

    if is_short_trading_day(today):
        return 19  # Short trading day close (example 19:30)

    return 22  # Normal close

def is_no_real_trading():
    # Simulate check: in real use, connect to volume/price data
    # This should check volume, volatility, or candles from yfinance or broker API
    # For now, always return False (assume market is active)
    return False
