# macro.py

import yfinance as yf
from datetime import datetime, timedelta


    if len(data) < 2:
        return "לא זמין"

    ma_20 = data["Close"].rolling(window=20).mean()

    if data["Close"].iloc[-1] > ma_20.iloc[-1]:
        return "עלייה"
    elif data["Close"].iloc[-1] < ma_20.iloc[-1]:
        return "ירידה"
    else:
        return "ניטרלי"

def get_pe_ratio_sp500():
    try:
        pe_data = yf.Ticker("^GSPC").info
        return round(pe_data.get("trailingPE", 0), 2)
    except:
        return "לא זמין"

def get_vix_trend():
    data = yf.download("^VIX", period="6mo")

    if len(data) < 2:
        return {"daily": "לא זמין"}

    ma_20 = data["Close"].rolling(window=20).mean()

    if data["Close"].iloc[-1] > ma_20.iloc[-1]:
        return {"daily": "עלייה"}
    elif data["Close"].iloc[-1] < ma_20.iloc[-1]:
        return {"daily": "ירידה"}
    else:
        return {"daily": "ניטרלי"}

def get_macro_summary():
    sp_trend_d = get_index_trend("^GSPC", "3mo")
    sp_trend_w = get_index_trend("^GSPC", "6mo")
    sp_trend_m = get_index_trend("^GSPC", "1y")

    nasdaq_trend_d = get_index_trend("^IXIC", "3mo")
    nasdaq_trend_w = get_index_trend("^IXIC", "6mo")
    nasdaq_trend_m = get_index_trend("^IXIC", "1y")

    pe_ratio = get_pe_ratio_sp500()
    vix = get_vix_trend()

    return {
        "sp500": {
            "daily": sp_trend_d,
            "weekly": sp_trend_w,
            "monthly": sp_trend_m,
        },
        "nasdaq": {
            "daily": nasdaq_trend_d,
            "weekly": nasdaq_trend_w,
            "monthly": nasdaq_trend_m,
        },
        "pe_ratio": pe_ratio,
        "vix_trend": vix,
    }

def is_market_bullish(summary):
    return (
        summary["sp500"]["daily"] == "עלייה"
        and summary["nasdaq"]["daily"] == "עלייה"
        and summary["vix_trend"]["daily"] == "ירידה"
    )
