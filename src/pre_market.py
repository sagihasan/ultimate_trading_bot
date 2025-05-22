import os
import yfinance as yf
from datetime import datetime, timedelta
from discord_manager import send_error_message
from discord_manager import send_public_message

def check_pre_market_alert(ticker):
    try:
        stock = yf.Ticker(ticker)
        pre_market_data = stock.history(period="1d", interval="5m", prepost=True)

        if pre_market_data.empty:
            return

        now = datetime.utcnow()
        current_price = pre_market_data["Close"].iloc[-1]
        open_price = pre_market_data["Open"].iloc[0]

        change_pct = ((current_price - open_price) / open_price) * 100

        if abs(change_pct) > 2:
            direction = "עלייה" if change_pct > 0 else "ירידה"
            message = f"""**התראה מוקדמת – פרה־מרקט**
המניה **{ticker}** ב{direction} של {round(change_pct, 2)}%
הבוט מזהה שינוי חד לפני פתיחת המסחר – נא להיערך בהתאם
"""
            send_message_with_delay(send_public_message, message)

    except Exception as e:
        send_error_message(f"שגיאה בפרה־מרקט ({ticker}): {e}")
