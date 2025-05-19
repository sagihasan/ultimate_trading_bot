# macro.py

import yfinance as yf
from investpy import get_macro_events
from datetime import datetime, timedelta


def get_macro_data():
    today = datetime.now().date()
    events = get_macro_events(today)
    return events


def get_index_trend(ticker, period="6mo"):
    data = yf.download(ticker, period=period)

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
        return {"daily": "לא זמין", "weekly": "לא זמין"}

    daily_trend = "ירידה" if data["Close"].iloc[-1] < data["Close"].iloc[-2] else "עלייה"
    weekly_ma = data["Close"].rolling(window=20).mean()
    weekly_trend = "ירידה" if data["Close"].iloc[-1] < weekly_ma.iloc[-1] else "עלייה"

    return {"daily": daily_trend, "weekly": weekly_trend}


def summarize_macro_trend():
    sp_trend_d = get_index_trend("^GSPC", period="1mo")
    sp_trend_w = get_index_trend("^GSPC", period="6mo")
    sp_trend_m = get_index_trend("^GSPC", period="1y")

    nasdaq_trend_d = get_index_trend("^IXIC", period="1mo")
    nasdaq_trend_w = get_index_trend("^IXIC", period="6mo")
    nasdaq_trend_m = get_index_trend("^IXIC", period="1y")

    pe_ratio = get_pe_ratio_sp500()
    vix = get_vix_trend()

    return {
        "sp500": {
            "daily": sp_trend_d,
            "weekly": sp_trend_w,
            "monthly": sp_trend_m
        },
        "nasdaq": {
            "daily": nasdaq_trend_d,
            "weekly": nasdaq_trend_w,
            "monthly": nasdaq_trend_m
        },
        "pe_ratio": pe_ratio,
        "vix_trend": vix
    }


def is_market_bullish(summary):
    return (
        summary["sp500"]["daily"] == "עלייה" and
        summary["nasdaq"]["daily"] == "עלייה" and
        summary["vix_trend"]["daily"] == "ירידה"
    )
