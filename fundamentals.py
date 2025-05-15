import requests
import os

ALPHA_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_fundamentals(symbol):
    fundamentals = {}
    try:
        url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_API_KEY}"
        response = requests.get(url)
        data = response.json()

        market_cap = float(data.get("MarketCapitalization", 0))
        revenue = float(data.get("RevenueTTM", 0))
        net_income = float(data.get("NetIncomeTTM", 0))
        eps = float(data.get("EPS", 0))
        pe_ratio = float(data.get("PERatio", 0))

        growth_type = "נייטרלית"
        if revenue > 0 and net_income > 0 and eps > 0:
            growth_type = "צמיחה"
        elif revenue < 0 or net_income < 0:
            growth_type = "צניחה"

        in_buffett_zone = (pe_ratio > 0 and pe_ratio < 15 and market_cap > 1_000_000_000 and net_income > 0)

        fundamentals = {
            "market_cap": market_cap,
            "revenue": revenue,
            "net_income": net_income,
            "eps": eps,
            "pe_ratio": pe_ratio,
            "growth_type": growth_type,
            "in_buffett_zone": in_buffett_zone
        }

    except Exception as e:
        print(f"שגיאה בפונדומנטלים ({symbol}): {e}")

    try:
        news_url = f"https://newsapi.org/v2/everything?q={symbol}&language=en&sortBy=publishedAt&pageSize=10&apiKey={NEWS_API_KEY}"
        news_response = requests.get(news_url)
        articles = news_response.json().get("articles", [])

        positive = 0
        negative = 0
        for article in articles:
            content = (article.get("title", "") + " " + article.get("description", "")).lower()
            if any(word in content for word in ["gain", "rise", "growth", "positive", "strong", "beat"]):
                positive += 1
            elif any(word in content for word in ["drop", "fall", "loss", "lawsuit", "bad", "negative"]):
                negative += 1

        sentiment = "ניטרלי"
        if positive > negative:
            sentiment = "חיובי"
        elif negative > positive:
            sentiment = "שלילי"

        fundamentals["sentiment"] = sentiment

    except Exception as e:
        fundamentals["sentiment"] = "לא זמין"
        print(f"שגיאה בסנטימנט: {e}")

    return fundamentals

