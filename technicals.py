# technicals.py

import yfinance as yf
import pandas as pd
import talib
import numpy as np

def calculate_indicators(df):
    df['EMA9'] = talib.EMA(df['Close'], timeperiod=9)
    df['EMA20'] = talib.EMA(df['Close'], timeperiod=20)
    df['EMA50'] = talib.EMA(df['Close'], timeperiod=50)
    df['EMA100'] = talib.EMA(df['Close'], timeperiod=100)
    df['EMA200'] = talib.EMA(df['Close'], timeperiod=200)

    df['RSI'] = talib.RSI(df['Close'], timeperiod=14)
    df['MACD'], df['MACD_signal'], _ = talib.MACD(df['Close'])

    upper, middle, lower = talib.BBANDS(df['Close'], timeperiod=20)
    df['BB_upper'] = upper
    df['BB_middle'] = middle
    df['BB_lower'] = lower

    df['Volume_SMA_20'] = talib.SMA(df['Volume'], timeperiod=20)
    df['Volume_Spike'] = df['Volume'] > 1.5 * df['Volume_SMA_20']

    df['MA_Cross'] = (df['EMA9'] > df['EMA20']) & (df['EMA9'].shift(1) <= df['EMA20'].shift(1))

    return df

def fetch_and_analyze_stock(ticker):
    timeframes = {
        "daily": "1d",
        "weekly": "1wk",
        "monthly": "1mo"
    }
    
    analyzed_data = {}
    for name, interval in timeframes.items():
        df = yf.download(ticker, period="6mo", interval=interval, progress=False)
        if df.empty or len(df) < 20:
            continue
        analyzed_data[name] = calculate_indicators(df)

    return analyzed_data
