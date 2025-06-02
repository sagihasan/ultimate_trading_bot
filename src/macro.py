# macro.py

import yfinance as yf
from datetime import datetime, timedelta


def get_index_trend(ticker, period="6mo"):
    try:
        data = yf.download(ticker, period=period)
        if data.empty or len(data) < 2:
            return "לא זמין"

        close = data["Close"].squeeze()
        ma_20 = close.rolling(window=20).mean()

        if close.iloc[-1] > ma_20.iloc[-1]:
            return "עלייה"
        elif close.iloc[-1] < ma_20.iloc[-1]:
            return "ירידה"
        else:
            return "ניטרלי"
    except Exception as e:
        print(f"שגיאה ב־{ticker}: {e}")
        return "לא זמין"


def get_pe_ratio_sp500():
    try:
        pe_data = yf.Ticker("^GSPC").info
        return round(pe_data.get("trailingPE", 0), 2)
    except:
        return "לא זמין"


def get_vix_trend():
    try:
        data = yf.download("^VIX", period="6mo")
        if data.empty or len(data) < 2:
            return {"daily": "לא זמין"}

        close = data["Close"].squeeze()
        ma_20 = close.rolling(window=20).mean()

        if close.iloc[-1] > ma_20.iloc[-1]:
            return {"daily": "עלייה"}
        elif close.iloc[-1] < ma_20.iloc[-1]:
            return {"daily": "ירידה"}
        else:
            return {"daily": "ניטרלי"}
    except:
        return {"daily": "לא זמין"}


def get_macro_summary():
    sp_trend_d = get_index_trend("^GSPC", period="1mo")
    sp_trend_w = get_index_trend("^GSPC", period="3mo")
    sp_trend_m = get_index_trend("^GSPC", period="6mo")

    nasdaq_trend_d = get_index_trend("^IXIC", period="1mo")
    nasdaq_trend_w = get_index_trend("^IXIC", period="3mo")
    nasdaq_trend_m = get_index_trend("^IXIC", period="6mo")

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
    return (summary["sp500"]["daily"] == "עלייה"
            and summary["nasdaq"]["daily"] == "עלייה"
            and summary["vix_trend"]["daily"] == "ירידה")


def detect_upcoming_crisis(events):
    crisis_keywords = [
        "משבר", "קריסה", "מיתון", "פשיטת רגל", "האטה", "אינפלציה"
    ]
    for event in events:
        if any(keyword in event.lower() for keyword in crisis_keywords):
            return True
    return False


def format_macro_summary(summary):
    return (f"""סיכום מאקרו:
מגמת S&P 500: {summary['sp500']['daily']}
מגמת נאסד״ק: {summary['nasdaq']['daily']}
מגמת VIX: {summary['vix_trend']['daily']}
מכפיל רווח S&P 500: {summary['pe_ratio']}""")
