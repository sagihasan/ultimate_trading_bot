import yfinance as yf
import pandas as pd
import pandas_ta
import numpy as np

# רשימת המניות לסריקה
STOCK_LIST = [
    'PLTR', 'AMZN', 'NVDA', 'AAPL', 'TSLA', 'ANET', 'SNEX', 'CRGY', 'MSFT', 'GOOG', 'AMD', 'ADBE', 'META', 'AI', 'AR',
    'ALSN', 'ASGN', 'HIMS', 'ASTS', 'HOOD', 'DKNG', 'SOUN', 'APP', 'PZZA', 'AVGO', 'SMCI', 'ADI', 'SEDG', 'ARKK', 'PERI',
    'NU', 'ACHC', 'SMMT', 'ZIM', 'GRPN', 'RKT', 'EBAY', 'CVNA', 'XBIT', 'PANW', 'NFLX', 'ABNB', 'BIDU', 'COIN', 'CRWD',
    'DDOG', 'DOCU', 'ETSY', 'FSLY', 'GDRX', 'GME', 'IQ', 'JD', 'LI', 'MELI', 'MGNI', 'MOMO', 'MRNA', 'NET', 'NIO', 'OKTA',
    'PDD', 'PINS', 'PTON', 'QCOM', 'ROKU', 'SHOP', 'SNAP', 'SQ', 'TAL', 'TDOC', 'TME', 'TWLO', 'U', 'UBER', 'VIPS',
    'WBA', 'WISH', 'WKHS', 'ZM', 'BABA', 'CSIQ', 'DKS', 'EA', 'ENPH', 'F', 'GM', 'GS', 'INTC', 'JNJ', 'KO', 'LMT', 'LOW',
    'LULU', 'MCD', 'MRK', 'MS', 'NVAX', 'ORCL', 'PEP', 'PYPL', 'SBUX', 'SJM', 'T', 'TSN', 'UNH', 'V', 'VZ', 'WMT', 'XOM',
    'BB', 'CLSK', 'RIOT', 'MARA', 'BTBT', 'HUT', 'BITF', 'CANO', 'SOFI', 'RIVN', 'LCID', 'AFRM', 'UPST', 'BMBL', 'MTCH',
    'CRSP'
]

def fetch_stock_data(symbol, period='6mo', interval='1d'):
    df = yf.download(symbol, period=period, interval=interval)
    return df

def analyze_stock(symbol):
    df = fetch_stock_data(symbol)
    if df.empty:
        return None

    # ממוצעים אקספוננציאליים
    df['EMA9'] = pandas_ta.ema(df['Close'], length=9)
    df['EMA20'] = pandas_ta.ema(df['Close'], length=20)
    df['EMA50'] = pandas_ta.ema(df['Close'], length=50)
    df['EMA100'] = pandas_ta.ema(df['Close'], length=100)
    df['EMA200'] = pandas_ta.ema(df['Close'], length=200)

    # אינדיקטורים נוספים
    df['RSI'] = pandas_ta.rsi(df['Close'], length=14)
    macd = pandas_ta.macd(df['Close'])
    df['MACD'] = macd['MACD_12_26_9']
    df['MACD_Signal'] = macd['MACDs_12_26_9']
    bb = pandas_ta.bbands(df['Close'], length=20)
    df['UpperBand'] = bb['BBU_20_2.0']
    df['LowerBand'] = bb['BBL_20_2.0']

    last = df.iloc[-1]

    signal = {
        'symbol': symbol,
        'price': last['Close'],
        'MA_Cross_Long': last['EMA9'] > last['EMA20'],
        'MA_Cross_Short': last['EMA9'] < last['EMA20'],
        'RSI': last['RSI'],
        'MACD_Bullish': last['MACD'] > last['MACD_Signal'],
        'MACD_Bearish': last['MACD'] < last['MACD_Signal'],
        'Above_Bollinger': last['Close'] > last['UpperBand'],
        'Below_Bollinger': last['Close'] < last['LowerBand']
    }

    return signal

def run_technical_analysis():
    results = []
    for stock in STOCK_LIST:
        print(f"Analyzing {stock}...")
        result = analyze_stock(stock)
        if result:
            results.append(result)
    return results
