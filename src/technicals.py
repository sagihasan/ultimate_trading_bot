import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator
from ta.volatility import BollingerBands


def analyze_technicals(df):
    result = {}

    if len(df) < 60:
        return None

    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    volume = df["Volume"]

    # RSI
    rsi = RSIIndicator(close=close, window=14)
    result["rsi"] = rsi.rsi().iloc[-1]

    # MACD
    macd = MACD(close=close)
    result["macd"] = macd.macd().iloc[-1]
    result["macd_signal"] = macd.macd_signal().iloc[-1]

    # EMA Cross
    ema_short = EMAIndicator(close=close, window=9).ema_indicator()
    ema_long = EMAIndicator(close=close, window=20).ema_indicator()
    result["ema_9"] = ema_short.iloc[-1]
    result["ema_20"] = ema_long.iloc[-1]
    result["ema_cross_up"] = ema_short.iloc[-2] < ema_long.iloc[
        -2] and ema_short.iloc[-1] > ema_long.iloc[-1]
    result["ema_cross_down"] = ema_short.iloc[-2] > ema_long.iloc[
        -2] and ema_short.iloc[-1] < ema_long.iloc[-1]

    # Trend
    trend = "none"
    if ema_short.iloc[-1] > ema_long.iloc[-1] and close.iloc[
            -1] > ema_short.iloc[-1]:
        trend = "bullish"
    elif ema_short.iloc[-1] < ema_long.iloc[-1] and close.iloc[
            -1] < ema_short.iloc[-1]:
        trend = "bearish"
    result["trend"] = trend

    # Bollinger Bands
    bb = BollingerBands(close=close, window=20, window_dev=2)
    result["bb_upper"] = bb.bollinger_hband().iloc[-1]
    result["bb_lower"] = bb.bollinger_lband().iloc[-1]

    # Indicators Summary
    result["indicators"] = {
        "rsi": round(result["rsi"], 2),
        "macd": round(result["macd"], 2),
        "macd_signal": round(result["macd_signal"], 2),
        "ema_cross_up": result["ema_cross_up"],
        "ema_cross_down": result["ema_cross_down"],
        "bb_upper": round(result["bb_upper"], 2),
        "bb_lower": round(result["bb_lower"], 2)
    }

    # Zones
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
    diff = high - low

    golden_zone_top = high - diff * 0.618
    golden_zone_bottom = high - diff * 0.786
    if golden_zone_bottom <= current_price <= golden_zone_top:
        result["in_golden_zone"] = True

    # Demand zone
    recent_lows = df.iloc[-20:]
    low_volume_zone = recent_lows[recent_lows["Low"] ==
                                  recent_lows["Low"].min()]
    if not low_volume_zone.empty and low_volume_zone["Volume"].iloc[0] > df[
            "Volume"].mean():
        result["in_demand_zone"] = True

    # Sentiment
    if current_price > df["Close"].rolling(20).mean().iloc[-1]:
        result["bullish"] = True
    elif current_price < df["Close"].rolling(20).mean().iloc[-1]:
        result["bearish"] = True

    return result

def calculate_fibonacci_levels(symbol):
    data = get_recent_candles(symbol)
    if len(data) < 60:
        return None

    high = max(candle['high'] for candle in data[-60:])
    low = min(candle['low'] for candle in data[-60:])
    diff = high - low

    return {
        "61.8%": round(high - diff * 0.618, 2),
        "78.6%": round(high - diff * 0.786, 2),
        "100%": round(low, 2)
    }


get_technical_summary = analyze_technicals
