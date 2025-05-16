# screener.py

import yfinance as yf
from discord_manager import send_discord_message
from stock_list import STOCK_LIST
import talib

def run_screener():
    strong_candidates = []

    for symbol in STOCK_LIST:
        try:
            data = yf.download(symbol, period="3mo", interval="1d", progress=False)
            if data.empty:
                continue

            close = data["Close"]
            volume = data["Volume"]
            ma20 = talib.SMA(close, timeperiod=20)
            avg_volume = volume.rolling(window=20).mean()

            latest_close = close[-1]
            latest_volume = volume[-1]

            price_above_ma = latest_close > ma20[-1]
            high_volume = latest_volume > avg_volume[-1] * 1.5

            if price_above_ma and high_volume:
                strong_candidates.append(symbol)

        except Exception as e:
            print(f"שגיאה בסריקת {symbol}: {e}")

    if strong_candidates:
        message = "**התראת סקרינר – מניות חזקות שבלטו היום:**\n"
        for s in strong_candidates:
            message += f"- {s}\n"
        send_discord_message(message)
    else:
        send_discord_message("**הסקרינר הסתיים – לא נמצאו מניות חזקות כרגע.**")
