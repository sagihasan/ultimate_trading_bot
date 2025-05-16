# fundamentals.py

import requests
import os
from datetime import datetime

ALPHA_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_fundamentals(symbol):
    fundamentals = {
        "market_cap": 0,
        "growth_type": "ניטרלית",
        "sentiment": "ניטרלי",
        "sentiment_score": 0.5,
        "in_buffett_zone": False
    }

    try:
        # שליפת נתוני דוח מאזני
        url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_API_KEY}"
        response = requests.get(url)
        data = response.json()

        fundamentals["market_cap"] = int(data.get("MarketCapitalization", 0))
        pe_ratio = float(data.get("PERatio", 0))
        revenue_growth = float(data.get("RevenueTTM", 0)) > 0
        net_income = float(data.get("ProfitMargin", 0)) > 0

        # סיווג צמיחה
        if revenue_growth and net_income:
            fundamentals["growth_type"] = "צמיחה"
        elif not revenue_growth and not net_income:
            fundamentals["growth_type"] = "צניחה"

        # בדיקת Buffett Zone (לדוגמה בלבד – תוכל לשנות ל־ fair value בהמשך)
        fundamentals["in_buffett_zone"] = pe_ratio < 15 and fundamentals["growth_type"] == "צמיחה"

    except Exception as e:
        print(f"שגיאה בנתונים פונדומנטליים: {e}")

    # ניתוח סנטימנט מ-NewsAPI
    try:
        news_url = f"https://newsapi.org/v2/everything?q={symbol}&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        response = requests.get(news_url)
        articles = response.json().get("articles", [])

        positive, negative = 0, 0
        for article in articles[:10]:
            title = article["title"].lower()
            if any(word in title for word in ["beats", "strong", "growth", "surge", "record"]):
                positive += 1
            elif any(word in title for word in ["misses", "weak", "loss", "drop", "down"]):
                negative += 1

        sentiment = "ניטרלי"
        score = 0.5
        if positive > negative:
            sentiment = "חיובי"
            score = 0.8
        elif negative > positive:
            sentiment = "שלילי"
            score = 0.2

        fundamentals["sentiment"] = sentiment
        fundamentals["sentiment_score"] = score

    except Exception as e:
        print(f"שגיאה בניתוח סנטימנט: {e}")

    return fundamentals

