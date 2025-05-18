import pandas as pd
import pandas_ta as ta

def analyze_technicals(df):
    result = {}

    close = df["Close"]
    volume = df["Volume"]

    # RSI
    result["rsi"] = ta.rsi(close, length=14).iloc[-1]

    # MACD
    macd = ta.macd(close)
    result["macd"] = macd["MACD_12_26_9"].iloc[-1] if "MACD_12_26_9" in macd else None
    result["macd_signal"] = macd["MACDs_12_26_9"].iloc[-1] if "MACDs_12_26_9" in macd else None

    # EMA Cross
    ema_short = ta.ema(close, length=9)
    ema_long = ta.ema(close, length=20)
    if ema_short is not None and ema_long is not None:
        result["ma_cross"] = int(ema_short.iloc[-1] > ema_long.iloc[-1])

    # Bollinger Bands
    bbands = ta.bbands(close)
    result["boll_upper"] = bbands["BBU_20_2.0"].iloc[-1] if "BBU_20_2.0" in bbands else None
    result["boll_middle"] = bbands["BBM_20_2.0"].iloc[-1] if "BBM_20_2.0" in bbands else None
    result["boll_lower"] = bbands["BBL_20_2.0"].iloc[-1] if "BBL_20_2.0" in bbands else None

    # Volume
    result["volume"] = volume.iloc[-1]

    return result
