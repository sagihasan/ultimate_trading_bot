# screener.py

import yfinance as yf
import pandas as pd

def detect_unusual_volume(stock_list, volume_threshold=1.5):
    unusual_stocks = []

    for symbol in stock_list:
        try:
            data = yf.download(symbol, period="30d", interval="1d", progress=False)
            if data is None or data.empty:
                continue

            data['avg_volume'] = data['Volume'].rolling(window=20).mean()
            latest_volume = data['Volume'].iloc[-1]
            avg_volume = data['avg_volume'].iloc[-1]

            if avg_volume and latest_volume > volume_threshold * avg_volume:
                unusual_stocks.append(symbol)

        except Exception as e:
            print(f"שגיאה בנתוני {symbol}: {e}")

    return unusual_stocks
