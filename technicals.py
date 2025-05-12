import yfinance as yf
import pandas as pd
import numpy as np
import talib
from config import STOCK_LIST


def run_technical_analysis(stock_list):
    results = []
    for symbol in stock_list:
        try:
            df = yf.download(symbol, period="6mo", interval="1d")
            if df.empty or len(df) < 50:
                continue

            df.dropna(inplace=True)
            close = df["Close"]
            high = df["High"]
            low = df["Low"]

            score = 0
            reasons = []

            # EMA conditions
            ema9 = talib.EMA(close, timeperiod=9)
            ema20 = talib.EMA(close, timeperiod=20)
            ema50 = talib.EMA(close, timeperiod=50)
            if close.iloc[-1] > ema9.iloc[-1]:
                score += 1
                reasons.append("מעל EMA9")
            if close.iloc[-1] > ema20.iloc[-1]:
                score += 1
                reasons.append("מעל EMA20")
            if talib.CDLHAMMER(open=df["Open"], high=high, low=low, close=close)[-1] != 0:
                score += 1
                reasons.append("נר היפוך")
            rsi = talib.RSI(close, timeperiod=14)
            if rsi.iloc[-1] > 50:
                score += 1
                reasons.append("RSI חיובי")
            macd, signal, _ = talib.MACD(close)
            if macd.iloc[-1] > signal.iloc[-1]:
                score += 1
                reasons.append("MACD חיובי")

            results.append({
                "symbol": symbol,
                "score": score,
                "reasons": reasons,
            })

        except Exception as e:
            print(f"שגיאה בטכני עבור {symbol}: {e}")

    return results

