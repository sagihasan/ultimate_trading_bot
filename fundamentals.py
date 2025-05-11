import yfinance as yf

def fetch_fundamentals(symbol):
    ticker = yf.Ticker(symbol)
    info = ticker.info

    market_cap = info.get('marketCap')
if market_cap is None:
    return None

    fundamentals = {
        'symbol': symbol,
        'market_cap': info.get('marketCap'),
        'eps': info.get('trailingEps'),
        'net_income': info.get('netIncomeToCommon'),
        'total_revenue': info.get('totalRevenue'),
        'sector': info.get('sector'),
        'future_outlook': analyze_future(info)
    }
    return fundamentals

def analyze_future(info):
    # דוגמה לצפי עתידי – תוכל לשדרג לפי הצורך:
    earnings_growth = info.get('earningsQuarterlyGrowth', 0)
    if earnings_growth > 0.15:
        return "החברה בצמיחה חזקה צפויה להמשיך לעלות"
    elif 0 < earnings_growth <= 0.15:
        return "החברה בצמיחה מתונה"
    elif earnings_growth < 0:
        return "החברה בירידה – להיזהר"
    else:
        return "אין מספיק מידע לצפי ברור"

def analyze_fundamentals():
    # דוגמה: אתה יכול להכניס כאן מניה לבדיקה קבועה או להעביר את זה מה-main
    result = fetch_fundamentals('AAPL')  # דוגמה עם AAPL
    status = result['market_cap'] is not None
    return {'status': status, 'future_outlook': result['future_outlook']}
