# technicals.py – ניתוח טכני מתקדם עם אינדיקטורים חובה, נרות היפוך, מגמות, ATR, EMA9, מינוף, תבניות וציון כללי

import yfinance as yf
import pandas as pd
import ta
from config import STOCK_LIST

# זיהוי נר היפוך פשוט (Hammer / Shooting Star)
def detect_reversal_candle(df):
    last = df.iloc[-1]
    body = abs(last['Close'] - last['Open'])
    range_ = last['High'] - last['Low']
    upper_shadow = last['High'] - max(last['Close'], last['Open'])
    lower_shadow = min(last['Close'], last['Open']) - last['Low']

    if lower_shadow > 2 * body and upper_shadow < body:
        return "Hammer"
    elif upper_shadow > 2 * body and lower_shadow < body:
        return "Shooting Star"
    else:
        return None

# קביעת מגמה לפי ממוצעים נעים אקספוננציאליים (EMA)
def determine_trend(df):
    ema50 = df['Close'].ewm(span=50, adjust=False).mean()
    ema200 = df['Close'].ewm(span=200, adjust=False).mean()
    if ema50.iloc[-1] > ema200.iloc[-1]:
        return "מגמת עלייה"
    elif ema50.iloc[-1] < ema200.iloc[-1]:
        return "מגמת ירידה"
    else:
        return "ניטרלי"

# זיהוי פסגות ותחתיות היפוך
def detect_peaks_valleys(df):
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(df['Close'], distance=5)
    valleys, _ = find_peaks(-df['Close'], distance=5)
    return len(peaks) > 0 and len(valleys) > 0

# זיהוי תבניות דגל/משולש
def detect_flag_or_triangle(df):
    recent = df['Close'].iloc[-10:]
    volatility = recent.max() - recent.min()
    avg_range = df['Close'].diff().abs().tail(10).mean()
    if volatility < 2 * avg_range:
        return True
    return False

# הפונקציה הראשית שמחזירה ניתוח טכני חכם
def run_technical_analysis(symbols):
    results = []
    for symbol in symbols:
        try:
            df = yf.download(symbol, period="6mo", interval="1d")
            df.dropna(inplace=True)

            rsi = ta.momentum.RSIIndicator(df['Close']).rsi()
            macd = ta.trend.MACD(df['Close'])
            macd_line = macd.macd()
            macd_signal = macd.macd_signal()

            ema9 = df['Close'].ewm(span=9, adjust=False).mean()
            ema20 = df['Close'].ewm(span=20, adjust=False).mean()
            ema50 = df['Close'].ewm(span=50, adjust=False).mean()

            atr = ta.volatility.AverageTrueRange(df['High'], df['Low'], df['Close']).average_true_range()
            atr_last = atr.iloc[-1] if not atr.empty else 0

            can_leverage = atr_last < df['Close'].iloc[-1] * 0.05

            conditions = {
                "RSI מעל 50": rsi.iloc[-1] > 50,
                "MACD מעל קו אות": macd_line.iloc[-1] > macd_signal.iloc[-1],
                "EMA9 מעל EMA20": ema9.iloc[-1] > ema20.iloc[-1],
                "EMA20 מעל EMA50": ema20.iloc[-1] > ema50.iloc[-1],
                "ATR נמוך מדי למנף": can_leverage,
                "מגמת עלייה": determine_trend(df) == "מגמת עלייה"
            }
            true_count = sum(conditions.values())
            score = round((true_count / len(conditions)) * 100)

            candle = detect_reversal_candle(df)
            reversal_zones = detect_peaks_valleys(df)
            pattern_flag = detect_flag_or_triangle(df)

            results.append({
                "symbol": symbol,
                "price": df['Close'].iloc[-1],
                "trend_daily": determine_trend(df),
                "trend_weekly": determine_trend(df[-5*4:]),
                "trend_monthly": determine_trend(df[-21*6:]),
                "candle_reversal": candle,
                "reversal_zone": reversal_zones,
                "pattern_flag_or_triangle": pattern_flag,
                "score": score,
                "atr": atr_last,
                "can_leverage": can_leverage,
                "conditions": conditions
            })
        except Exception as e:
            results.append({"symbol": symbol, "error": str(e)})
    return results

