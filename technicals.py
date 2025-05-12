import pandas as pd

try:
    import talib
    TALIB_AVAILABLE = True
except ImportError:
    import pandas_ta as ta
    TALIB_AVAILABLE = False

def run_technical_analysis(stock_list):
    results = []
    for stock in stock_list:
        try:
            df = stock["data"]  # הנחה שיש key בשם "data" עם DataFrame
            close = df["Close"]

            if TALIB_AVAILABLE:
                rsi = talib.RSI(close)
                macd, macdsignal, _ = talib.MACD(close)
            else:
                rsi = ta.rsi(close=close)
                macd_df = ta.macd(close=close)
                macd = macd_df["MACD_12_26_9"]
                macdsignal = macd_df["MACDs_12_26_9"]

            last_rsi = rsi.iloc[-1] if not rsi.isnull().all() else None
            last_macd = macd.iloc[-1] if not macd.isnull().all() else None
            last_signal = macdsignal.iloc[-1] if not macdsignal.isnull().all() else None

            score = 0
            if last_rsi and last_rsi > 50:
                score += 1
            if last_macd and last_signal and last_macd > last_signal:
                score += 1

            results.append({
                "symbol": stock["symbol"],
                "rsi": last_rsi,
                "macd": last_macd,
                "macd_signal": last_signal,
                "score": score
            })
        except Exception as e:
            print(f"שגיאה בניתוח טכני של {stock['symbol']}: {e}")

    return results

