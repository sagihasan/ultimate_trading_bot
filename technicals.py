# technicals.py

import yfinance as yf
import pandas as pd
import talib

def analyze_technicals(symbol):
    try:
        data = yf.download(symbol, period="6mo", interval="1d", progress=False)
        data.dropna(inplace=True)

        close = data["Close"]
        volume = data["Volume"]

        rsi = float(talib.RSI(close, timeperiod=14)[-1])
        macd, macdsignal, _ = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
        ma_9 = talib.EMA(close, timeperiod=9)
        ma_20 = talib.EMA(close, timeperiod=20)
        ma_cross = int(ma_9[-1] > ma_20[-1])

        # מגמה יומית / שבועית
        daily_trend = "לונג" if ma_9[-1] > ma_20[-1] else "שורט"
        weekly_data = yf.download(symbol, period="2y", interval="1wk", progress=False)
        weekly_ma = talib.EMA(weekly_data["Close"], timeperiod=9)
        weekly_trend = "לונג" if weekly_data["Close"][-1] > weekly_ma[-1] else "שורט"

        # Volume
        avg_volume = volume.rolling(window=20).mean()
        high_volume = volume[-1] > avg_volume[-1]

        # כניסה והגדרת אזור ביקוש
        entry_price = round(close[-1], 2)
        in_demand_zone = (close[-1] < ma_20[-1]) and (volume[-1] > avg_volume[-1])

        return {
            "rsi": round(rsi, 2),
            "macd": round(macd[-1] - macdsignal[-1], 4),
            "volume": int(volume[-1]),
            "ma_cross": ma_cross,
            "in_demand_zone": in_demand_zone,
            "entry_price": entry_price,
            "weekly_trend": weekly_trend,
            "daily_trend": daily_trend
        }

    except Exception as e:
        print(f"שגיאה בניתוח טכני ל־{symbol}: {e}")
        return {}
