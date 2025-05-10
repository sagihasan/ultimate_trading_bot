import yfinance as yf
import pandas as pd
import talib

# רשימת המניות לסריקה
STOCK_LIST = [
    'PLTR', 'AMZN', 'NVDA', 'AAPL', 'TSLA', 'ANET', 'SNEX', 'CRGY', 'MSFT', 'GOOG',
    'AMD', 'ADBE', 'META', 'AI', 'AR', 'ALSN', 'ASGN', 'HIMS', 'ASTS', 'HOOD',
    'DKNG', 'SOUN', 'APP', 'PZZA', 'AVGO', 'SMCI', 'ADI', 'SEDG', 'ARKK', 'PERI',
    'NU', 'ACHC', 'SMMT', 'ZIM', 'GRPN', 'RKT', 'EBAY', 'CVNA', 'XBI', 'PANW', 'NFLX'
]

def fetch_stock_data(symbol, period='6mo', interval='1d'):
    df = yf.download(symbol, period=period, interval=interval)
    return df

def analyze_stock(symbol):
    df = fetch_stock_data(symbol)
    if df.empty:
        return None

    df['MA9'] = talib.SMA(df['Close'], timeperiod=9)
    df['MA20'] = talib.SMA(df['Close'], timeperiod=20)
    df['MA50'] = talib.SMA(df['Close'], timeperiod=50)
    df['MA100'] = talib.SMA(df['Close'], timeperiod=100)
    df['MA200'] = talib.SMA(df['Close'], timeperiod=200)
    df['RSI'] = talib.RSI(df['Close'], timeperiod=14)
    macd, macdsignal, _ = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['MACD'] = macd
    df['MACD_Signal'] = macdsignal
    upperband, middleband, lowerband = talib.BBANDS(df['Close'], timeperiod=20)
    df['UpperBand'] = upperband
    df['MiddleBand'] = middleband
    df['LowerBand'] = lowerband

    # בדיקות של אינדיקטורים לדוגמה:
    last = df.iloc[-1]
    signal = {
        'symbol': symbol,
        'price': last['Close'],
        'MA_Cross_Long': last['MA9'] > last['MA20'],
        'MA_Cross_Short': last['MA9'] < last['MA20'],
        'RSI': last['RSI'],
        'MACD_Bullish': last['MACD'] > last['MACD_Signal'],
        'MACD_Bearish': last['MACD'] < last['MACD_Signal'],
        'Above_Bollinger': last['Close'] > last['UpperBand'],
        'Below_Bollinger': last['Close'] < last['LowerBand']
    }

    # כאן נוכל להוסיף את הזיהויים החכמים יותר כמו Golden Zone וכו'

    return signal

def run_technical_analysis():
    results = []
    for stock in STOCK_LIST:
        print(f"Analyzing {stock}...")
        result = analyze_stock(stock)
        if result:
            results.append(result)
    return results
