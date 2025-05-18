# macro.py

import yfinance as yf
from investing_scraper import get_macro_events
from datetime import datetime, timedelta

def get_macro_data():
    today = datetime.now().date()
    events = get_macro_events(today)
    return events

def get_index_trend(ticker, period="6mo"):
    data = yf.download(ticker, period=period)
    if len(data) < 2:
        return "לא ידוע"
    trend = "עולה" if data["Close"][-1] > data["Close"][0] else "יורד"
    return trend

def get_pe_ratio_sp500():
    try:
        pe = yf.Ticker("^GSPC").info.get("trailingPE", None)
        return round(pe, 2) if pe else "לא זמין"
    except:
        return "שגיאה"

def get_vix_trend():
    try:
        vix = yf.download("^VIX", period="6mo")
        if len(vix) < 2:
            return "לא ידוע"
        daily = "עולה" if vix["Close"][-1] > vix["Close"][-2] else "יורד"
        weekly = "עולה" if vix["Close"][-1] > vix["Close"][-5] else "יורד"
        monthly = "עולה" if vix["Close"][-1] > vix["Close"][-20] else "יורד"
        return {"daily": daily, "weekly": weekly, "monthly": monthly}
    except:
        return {"daily": "שגיאה", "weekly": "שגיאה", "monthly": "שגיאה"}

def detect_upcoming_crisis(events):
    for event in events:
        if event['impact'] == "High" and "rate" in event['title'].lower():
            return "אירוע רגיש מאוד: " + event['title']
    return None

def detect_gap_warning_from_macro(events):
    for event in events:
        if event['impact'] == "High" and any(term in event['title'].lower() for term in ["inflation", "interest", "gdp", "powell", "cpi", "ppi"]):
            return "צפוי גאפ משמעותי בעקבות: " + event['title']
    return None

def format_macro_summary():
    sp_trend_d = get_index_trend("^GSPC", "3mo")
    sp_trend_w = get_index_trend("^GSPC", "1y")
    sp_trend_m = get_index_trend("^GSPC", "5y")

    nasdaq_trend_d = get_index_trend("^IXIC", "3mo")
    nasdaq_trend_w = get_index_trend("^IXIC", "1y")
    nasdaq_trend_m = get_index_trend("^IXIC", "5y")

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
        summary["sp500"]["daily"] == "עולה" and
        summary["nasdaq"]["daily"] == "עולה" and
        summary["vix_trend"]["daily"] == "יורד"
    )
