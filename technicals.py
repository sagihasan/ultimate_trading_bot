import pandas as pd
import pandas_ta as ta

def analyze_technicals(df):
    result = {}

    if len(df) < 60:
        return None

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

    # EMA Cross
    ema_short = ta.ema(close, length=9)
    ema_long = ta.ema(close, length=20)
    result["ema_9"] = ema_short.iloc[-1]
    result["ema_20"] = ema_long.iloc[-1]
    result["ema_cross_up"] = ema_short.iloc[-2] < ema_long.iloc[-2] and ema_short.iloc[-1] > ema_long.iloc[-1]
    result["ema_cross_down"] = ema_short.iloc[-2] > ema_long.iloc[-2] and ema_short.iloc[-1] < ema_long.iloc[-1]

    # Trend: Simple logic using EMA alignment
    trend = "none"
    if ema_short.iloc[-1] > ema_long.iloc[-1] and close.iloc[-1] > ema_short.iloc[-1]:
        trend = "bullish"
    elif ema_short.iloc[-1] < ema_long.iloc[-1] and close.iloc[-1] < ema_short.iloc[-1]:
        trend = "bearish"
    result["trend"] = trend

    # Bollinger Bands
    bb = ta.bbands(close, length=20)
    result["bb_upper"] = bb["BBU_20_2.0"].iloc[-1]
    result["bb_lower"] = bb["BBL_20_2.0"].iloc[-1]

    # Indicators summary
    result["indicators"] = {
        "rsi": round(result["rsi"], 2),
        "macd": round(result["macd"], 2),
        "macd_signal": round(result["macd_signal"], 2),
        "ema_cross_up": result["ema_cross_up"],
        "ema_cross_down": result["ema_cross_down"],
        "bb_upper": round(result["bb_upper"], 2),
        "bb_lower": round(result["bb_lower"], 2)
    }

    # Zones and sentiment
    result["zones"] = identify_zones(df)

    return result


def identify_zones(df):
    result = {
        "in_golden_zone": False,
        "in_demand_zone": False,
        "bullish": False,
        "bearish": False
    }

    if len(df) < 60:
        return result

    high = df["High"].rolling(window=60).max().iloc[-1]
    low = df["Low"].rolling(window=60).min().iloc[-1]
    current_price = df["Close"].iloc[-1]

    # Golden Zone (Fibonacci retracement)
    diff = high - low
    golden_zone_top = high - diff * 0.618
    golden_zone_bottom = high - diff * 0.786

    if golden_zone_bottom <= current_price <= golden_zone_top:
        result["in_golden_zone"] = True

    # Demand Zone – recent low with high volume
    recent_lows = df.iloc[-20:]
    low_volume_zone = recent_lows[recent_lows["Low"] == recent_lows["Low"].min()]
    if not low_volume_zone.empty and low_volume_zone["Volume"].iloc[0] > df["Volume"].mean():
        result["in_demand_zone"] = True

    # Bullish/Bearish based on price vs. 20-period mean
    if current_price > df["Close"].rolling(20).mean().iloc[-1]:
        result["bullish"] = True
    elif current_price < df["Close"].rolling(20).mean().iloc[-1]:
        result["bearish"] = True

    return result
