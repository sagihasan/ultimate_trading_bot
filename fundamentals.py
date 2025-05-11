import yfinance as yf

def fetch_fundamentals(symbol):
    ticker = yf.Ticker(symbol)
    info = ticker.info

    # בדיקה: אם אין שווי שוק – עצור כאן
    market_cap = info.get('marketCap')
    if market_cap is None:
        return None

    fundamentals = {
        'symbol': symbol,
        'market_cap': market_cap,
        'eps': info.get('trailingEps'),
        'net_income': info.get('netIncomeToCommon'),
        'total_revenue': info.get('totalRevenue'),
        'sector': info.get('sector'),
        'future_outlook': analyze_future(info)
    }

    return fundamentals

def analyze_future(info):
    earnings_growth = info.get('earningsQuarterlyGrowth', 0)
    if earnings_growth > 0.15:
        return "צפי חיובי חזק להמשך מגמה"
    elif 0 < earnings_growth <= 0.15:
        return "צפי חיובי בינוני"
    elif earnings_growth < 0:
        return "צפי שלילי – להיזהר"
    else:
        return "אין צפי ברור לפי נתוני צמיחה"

def analyze_fundamentals():
    result = fetch_fundamentals("AAPL")  # דוגמה לבדיקה מקומית בלבד
    if result is None:
        return {"status": "אין נתונים"}
    status = result['market_cap']
    future_outlook = result['future_outlook']
    return {"status": status, "future_outlook": future_outlook}
