import yfinance as yf
import pandas as pd
import ta
from config import ACCOUNT_SIZE, RISK_PERCENTAGE, STOP_LOSS_PERCENT, TAKE_PROFIT_PERCENT


def run_technical_analysis(symbols):
    results = []
    for symbol in symbols:
        try:
            data = yf.download(symbol, period="6mo", interval="1d")
            if data.empty or len(data) < 50:
                continue

            df = data.copy()
            df.dropna(inplace=True)

            df["rsi"] = ta.momentum.RSIIndicator(close=df["Close"], window=14).rsi()
            df["macd"] = ta.trend.MACD(close=df["Close"]).macd_diff()
            df["ma50"] = ta.trend.SMAIndicator(close=df["Close"], window=50).sma_indicator()
            df["ma200"] = ta.trend.SMAIndicator(close=df["Close"], window=200).sma_indicator()
            df["bb_upper"] = ta.volatility.BollingerBands(close=df["Close"]).bollinger_hband()
            df["bb_lower"] = ta.volatility.BollingerBands(close=df["Close"]).bollinger_lband()
            df.dropna(inplace=True)

            latest = df.iloc[-1]
            previous = df.iloc[-2]

            score = 0

            if latest["rsi"] > 50:
                score += 1
            if latest["macd"] > 0 and previous["macd"] < 0:
                score += 1
            if latest["Close"] > latest["ma50"]:
                score += 1
            if latest["Close"] > latest["ma200"]:
                score += 1
            if latest["Close"] < latest["bb_upper"] and latest["Close"] > latest["bb_lower"]:
                score += 1

            if score >= 3:
                price = latest["Close"]
                stop_loss = round(price * (1 - STOP_LOSS_PERCENT / 100), 2)
                take_profit = round(price * (1 + TAKE_PROFIT_PERCENT / 100), 2)
                risk_amount = ACCOUNT_SIZE * (RISK_PERCENTAGE / 100)
                position_size = round(risk_amount / (price - stop_loss), 2)

                results.append({
                    "symbol": symbol,
                    "score": score,
                    "price": round(price, 2),
                    "stop_loss": stop_loss,
                    "take_profit": take_profit,
                    "position_size": position_size
                })
        except Exception as e:
            print(f"Error analyzing {symbol}: {e}")

    return sorted(results, key=lambda x: x["score"], reverse=True)

