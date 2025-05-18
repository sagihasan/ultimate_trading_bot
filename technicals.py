import pandas as pd
import pandas_ta as ta
from zones import identify_zones

def analyze_technicals(df):
    result = {}

    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    volume = df["Volume"]

    # RSI
    result["rsi"] = ta.rsi(close, length=14).iloc[-1]

    # MACD
    macd = ta.macd(close)
    result["macd"] = macd["MACD_12_26_9"].iloc[-1]
    result["macd_signal"] = macd["MACDs_12_26_9"].iloc[-1]

    # EMAs
    ema_9 = ta.ema(close, length=9)
    ema_20 = ta.ema(close, length=20)
    ema_50 = ta.ema(close, length=50)
    ema_100 = ta.ema(close, length=100)
    ema_200 = ta.ema(close, length=200)

    result["ema_9"] = ema_9.iloc[-1]
    result["ema_20"] = ema_20.iloc[-1]
    result["ema_50"] = ema_50.iloc[-1]
    result["ema_100"] = ema_100.iloc[-1]
    result["ema_200"] = ema_200.iloc[-1]

    # Bollinger Bands
    bb = ta.bbands(close)
    result["bb_upper"] = bb["BBU_20_2.0"].iloc[-1]
    result["bb_lower"] = bb["BBL_20_2.0"].iloc[-1]
    result["bb_mid"] = bb["BBM_20_2.0"].iloc[-1]
    result["bb_breakout"] = "above" if close.iloc[-1] > result["bb_upper"] else "below" if close.iloc[-1] < result["bb_lower"] else "inside"

    # Volume
    result["volume"] = volume.iloc[-1]

    # EMA Crosses
    result["ema_cross"] = {
        "9_20": "bullish" if result["ema_9"] > result["ema_20"] else "bearish",
        "20_50": "bullish" if result["ema_20"] > result["ema_50"] else "bearish",
        "50_200": "bullish" if result["ema_50"] > result["ema_200"] else "bearish"
    }

    # Price Crosses
    yesterday = close.iloc[-2]
    today = close.iloc[-1]
    result["price_cross"] = {
        "ema_9": "up" if yesterday < result["ema_9"] and today > result["ema_9"] else "down" if yesterday > result["ema_9"] and today < result["ema_9"] else "none",
        "ema_20": "up" if yesterday < result["ema_20"] and today > result["ema_20"] else "down" if yesterday > result["ema_20"] and today < result["ema_20"] else "none",
        "ema_50": "up" if yesterday < result["ema_50"] and today > result["ema_50"] else "down" if yesterday > result["ema_50"] and today < result["ema_50"] else "none"
    }

    # Trend Direction
    result["trend"] = "long" if result["ema_9"] > result["ema_20"] and result["macd"] > result["macd_signal"] else "short"

    # Bullish / Bearish / Mixed
    result["trend_sentiment"] = (
        "Bullish" if result["ema_9"] > result["ema_20"] > result["ema_50"] and result["macd"] > result["macd_signal"]
        else "Bearish" if result["ema_9"] < result["ema_20"] < result["ema_50"] and result["macd"] < result["macd_signal"]
        else "Mixed"
    )

    # Summary
    result["indicators"] = {
        "rsi": round(result["rsi"], 2),
        "macd": round(result["macd"], 2),
        "macd_signal": round(result["macd_signal"], 2),
        "ema_cross": result["ema_cross"],
        "price_cross": result["price_cross"],
        "bollinger": result["bb_breakout"]
    }

    # Zones
    result["zones"] = identify_zones(df)

    return result
