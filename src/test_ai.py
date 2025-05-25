from ml_model import calculate_ai_score

features = {
    "rsi": 58,
    "macd": 0.4,
    "volume": 1700000,
    "ma_cross": 1,
    "in_demand_zone": 1,
    "in_buffett_zone": 1,
    "sentiment_score": 0.75,
    "weekly_trend": 1,
    "daily_trend": 1
}

result = calculate_ai_score(features)
print(result)
