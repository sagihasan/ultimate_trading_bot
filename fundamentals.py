import yfinance as yf
from datetime import datetime, timedelta
import requests

def analyze_fundamentals(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        market_cap = info.get("marketCap", 0)
        pe_ratio = info.get("trailingPE", 0)
        forward_pe = info.get("forwardPE", 0)
        earnings_growth = info.get("earningsQuarterlyGrowth", 0)
        sector = info.get("sector", "לא ידוע")

        # תחזית פונדומנטלית כללית
        if market_cap > 10_000_000_000 and earnings_growth > 0:
            trend = "צמיחה"
        elif earnings_growth < 0:
            trend = "צניחה"
        else:
            trend = "ניטרלי"

        # ניקוד פונדומנטלי לצורך AI
        score = 0
        if market_cap > 5_000_000_000:
            score += 25
        if pe_ratio > 0 and pe_ratio < 30:
            score += 25
        if earnings_growth > 0:
            score += 25
        if forward_pe and forward_pe < pe_ratio:
            score += 25

        return {
            "market_cap": market_cap,
            "pe_ratio": pe_ratio,
            "forward_pe": forward_pe,
            "earnings_growth": earnings_growth,
            "sector": sector,
            "trend": trend,
            "fundamental_score": score
        }

    except Exception as e:
        print(f"שגיאה בניתוח פונדומנטלי עבור {ticker}: {e}")
        return None

def check_upcoming_earnings(ticker):
    try:
        stock = yf.Ticker(ticker)
        earnings_date = stock.calendar.get('Earnings Date')
        if earnings_date is not None:
            now = datetime.now().date()
            earnings_day = earnings_date[0].date()
            delta_days = (earnings_day - now).days
            return earnings_day, delta_days
        return None, None
    except Exception as e:
        print(f"שגיאה בבדיקת דוח קרוב עבור {ticker}: {e}")
        return None, None
