import yfinance as yf
import ta

STOCK_LIST = [
    'PLTR', 'AMZN', 'NVDA', 'AAPL', 'TSLA', 'ANET', 'SNEX', 'CRGY',
    'MSFT', 'GOOG', 'AMD', 'ADBE', 'META', 'AI', 'AR', 'ALSN', 'ASGN',
    'HIMS', 'ASTS', 'HOOD', 'DKNG', 'SOUN', 'APP', 'PZZA', 'AVGO', 'SMCI',
    'ADI', 'SEDG', 'ARKK', 'PERI', 'NU', 'ACHC', 'SMMT', 'ZIM', 'GRPN',
    'RKT', 'EBAY', 'CVNA', 'XBI', 'PANW', 'NFLX', 'ABNB', 'BIDU', 'COIN',
    'CRWD', 'DDOG', 'DOCU', 'ETSY', 'FSLY', 'GDRX', 'GME', 'IQ', 'JD',
    'LI', 'MELI', 'MGNI', 'MOMO', 'MRNA', 'NET', 'NIO', 'OKTA', 'PDD',
    'PINS', 'PTON', 'QCOM', 'ROKU', 'SHOP', 'SNAP', 'SQ', 'TAL', 'TDOC',
    'TME', 'TWLO', 'U', 'UBER', 'VIPS', 'WBA', 'WISH', 'WKHS', 'ZM',
    'BABA', 'CSIQ', 'DKS', 'EA', 'ENPH', 'F', 'GM', 'GS', 'INTC', 'JNJ',
    'KO', 'LMT', 'LOW', 'LULU', 'MCD', 'MRK', 'MS', 'NVAX',
    'ORCL', 'PEP', 'PYPL', 'SBUX', 'SJM', 'T', 'TSN', 'UNH', 'V', 'VZ',
    'WMT', 'XOM', 'BB', 'CLSK', 'RIOT', 'MARA', 'BTBT', 'HUT', 'BITF',
    'CANO', 'SOFI', 'RIVN', 'LCID', 'AFRM', 'UPST', 'BMBL', 'MTCH', 'CRSP'
]

def fetch_data(symbol, period, interval):
    return yf.download(symbol, period=period, interval=interval)

def detect_trend(df):
    ema9 = ta.trend.ema_indicator(df['Close'], window=9).ema_indicator()
    ema20 = ta.trend.ema_indicator(df['Close'], window=20).ema_indicator()
    return "מגמת עלייה" if ema9.iloc[-1] > ema20.iloc[-1] else "מגמת ירידה"

def analyze_stock(symbol):
    daily = fetch_data(symbol, "6mo", "1d")
    weekly = fetch_data(symbol, "2y", "1wk")
    monthly = fetch_data(symbol, "10y", "1mo")

    if daily.empty or weekly.empty or monthly.empty:
        return None

    return {
        "symbol": symbol,
        "price": daily["Close"].iloc[-1],
        "trend_daily": detect_trend(daily),
        "trend_weekly": detect_trend(weekly),
        "trend_monthly": detect_trend(monthly)
    }

def run_technical_analysis():
    results = []
    for symbol in STOCK_LIST:
        print(f"Analyzing {symbol}...")
        result = analyze_stock(symbol)
        if result:
            results.append(result)
    return results
