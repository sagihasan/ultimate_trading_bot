# price_utils.py

import yfinance as yf

def get_current_price(symbol):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d", interval="1m")
        if data.empty:
            return 0.0
        return float(data["Close"].iloc[-1])
    except Exception as e:
        print(f"שגיאה בשליפת מחיר נוכחי עבור {symbol}: {e}")
        return 0.0
