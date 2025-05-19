import yfinance as yf
from datetime import datetime
import investpy

def get_index_trend(ticker, period="6mo"):
    data = yf.download(ticker, period=period)
    if len(data) < 2:
        return "לא ידוע"
    last = data["Close"].iloc[-1]
    prev = data["Close"].iloc[0]
    if last > prev:
        return "עלייה"
    elif last < prev:
        return "ירידה"
    else:
        return "צדדי"

def get_vix_trend():
    return {
        "daily": get_index_trend("^VIX", "1mo"),
        "weekly": get_index_trend("^VIX", "3mo"),
        "monthly": get_index_trend("^VIX", "6mo"),
    }

def get_pe_ratio_sp500():
    try:
        data = investpy.get_stock_information(stock='SPY', country='united states')
        return float(data['P/E'].values[0])
    except Exception:
        return None

def get_macro_summary():
    sp_trend_d = get_index_trend("^GSPC", "1mo")
    sp_trend_w = get_index_trend("^GSPC", "3mo")
    sp_trend_m = get_index_trend("^GSPC", "6mo")

    nasdaq_trend_d = get_index_trend("^IXIC", "1mo")
    nasdaq_trend_w = get_index_trend("^IXIC", "3mo")
    nasdaq_trend_m = get_index_trend("^IXIC", "6mo")

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
