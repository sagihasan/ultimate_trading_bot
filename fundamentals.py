import requests
import os

ALPHA_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_fundamentals(symbol):
    fundamentals = {}
    try:
        # שליפה מ-Alpha Vantage
        url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_API_KEY}"
        response = requests.get(url)
        data = response.json()

        market_cap = float(data.get("MarketCapitalization", 0))
        revenue = float(data.get("RevenueTTM", 0))
        net_income = float(data.get("NetIncomeTTM", 0))
        eps = float(data.get("EPS", 0))

        growth_type = "נייטרלית"
        if revenue > 0 and net_income > 0 and eps > 0:
            growth_type = "צמיחה"
        elif revenue < 0 or net_income < 0:
            growth_type = "צניחה"

        fundamentals = {
            "market_cap": market_cap,
            "revenue": revenue,
            "net_income": net_income,
            "eps": eps,
            "growth_type": growth_type
        }

    except Exception as e:
        print(f"שגיאה בשליפת נתונים פונדומנטליים: {e}")

    try:
        # שליפת סנטימנט מ-NewsAPI
        news_url = f"https://newsapi.org/v2/everything?q={symbol}&language=en&sortBy=publishedAt&pageSize=10&apiKey={NEWS_API_KEY}"
        news_response = requests.get(news_url)
        articles = news_response.json().get("articles", [])

        negative = 0
        positive = 0

        for article in articles:
            title = article.get("title", "").lower()
            description = article.get("description", "").lower()
            content = f"{title} {description}"
            if any(word in content for word in ["drop", "fall", "loss", "lawsuit", "bad", "negative", "decline"]):
                negative += 1
            elif any(word in content for word in ["gain", "rise", "growth", "positive", "strong", "beat", "upside"]):
                positive += 1

        sentiment = "ניטרלי"
        if positive > negative:
            sentiment = "חיובי"
        elif negative > positive:
            sentiment = "שלילי"

        fundamentals["sentiment"] = sentiment

    except Exception as e:
        print(f"שגיאה בשליפת סנטימנט חדשותי: {e}")
        fundamentals["sentiment"] = "לא זמין"

    return fundamentals

