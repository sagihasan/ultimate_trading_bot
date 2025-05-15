import yfinance as yf
import pandas as pd
import ta
from config import ACCOUNT_SIZE, RISK_PERCENTAGE, STOP_LOSS_PERCENT, TAKE_PROFIT_PERCENT
from utils import log_error

def run_technical_analysis(symbols):
    results = []

    for symbol in symbols:
        try:
            data = yf.download(symbol, period="6mo", interval="1d", progress=False)
            if data.empty or len(data) < 50:
                continue

            df = data.copy()
            df.dropna(inplace=True)

            # Indicators using Exponential Moving Averages (EMA)
            df["ema50"] = ta.trend.EMAIndicator(close=df["Close"], window=50).ema_indicator()
            df["ema200"] = ta.trend.EMAIndicator(close=df["Close"], window=200).ema_indicator()
            df["rsi"] = ta.momentum.RSIIndicator(close=df["Close"], window=14).rsi()
            df["macd"] = ta.trend.MACD(close=df["Close"]).macd_diff()
            bb = ta.volatility.BollingerBands(close=df["Close"])
            df["bb_upper"] = bb.bollinger_hband()
            df["bb_lower"] = bb.bollinger_lband()

            df.dropna(inplace=True)

            latest = df.iloc[-1]
            previous = df.iloc[-2]

            score = 0
            if latest["rsi"] > 50:
                score += 1
            if latest["macd"] > 0 and previous["macd"] < 0:
                score += 1
            if latest["Close"] > latest["ema50"]:
                score += 1
            if latest["Close"] > latest["ema200"]:
                score += 1
            if latest["Close"] < latest["bb_upper"] and latest["Close"] > latest["bb_lower"]:
                score += 1

            if score >= 3:
                price = latest["Close"]
                stop_loss = round(price * (1 - STOP_LOSS_PERCENT / 100), 2)
                take_profit = round(price * (1 + TAKE_PROFIT_PERCENT / 100), 2)
                risk_amount = ACCOUNT_SIZE * (RISK_PERCENTAGE / 100)
                position_size = round(risk_amount / max(price - stop_loss, 0.01), 2)

                results.append({
                    "symbol": symbol,
                    "score": score,
                    "price": round(price, 2),
                    "stop_loss": stop_loss,
                    "take_profit": take_profit,
                    "position_size": position_size
                })

        except Exception as e:
            log_error(f"שגיאה בניתוח טכני עבור {symbol}: {str(e)}")

    return sorted(results, key=lambda x: x["score"], reverse=True)
