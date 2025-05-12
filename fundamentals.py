import requests
from config import ALPHA_VANTAGE_API_KEY, NEWS_API_KEY

def analyze_fundamentals(stock_list):
    results = {}
    for symbol in stock_list:
        try:
            overview = fetch_company_overview(symbol)
            news_sentiment = fetch_news_sentiment(symbol)

            if not overview:
                continue

            market_cap = float(overview.get("MarketCapitalization", 0))
            revenue = float(overview.get("RevenueTTM", 0))
            net_income = float(overview.get("NetIncomeTTM", 0))
            sector = overview.get("Sector", "Unknown")

            trend = "צמיחה" if net_income > 0 and revenue > 0 else "צניחה" if net_income < 0 else "ניטרלי"

            results[symbol] = {
                "market_cap": market_cap,
                "revenue": revenue,
                "net_income": net_income,
                "sector": sector,
                "trend": trend,
                "sentiment": news_sentiment,
            }

        except Exception as e:
            print(f"שגיאה בניתוח {symbol}: {e}")

    return results


def fetch_company_overview(symbol):
    try:
        url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json()
        return data if "Symbol" in data else None
    except Exception as e:
        print(f"שגיאה ב־Alpha Vantage עבור {symbol}: {e}")
        return None


def fetch_news_sentiment(symbol):
    try:
        url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}"
        response = requests.get(url, timeout=10)
        articles = response.json().get("articles", [])
        positive, negative = 0, 0

        for article in articles[:5]:
            title = article.get("title", "").lower()
            if any(word in title for word in ["beats", "growth", "strong", "gain"]):
                positive += 1
            if any(word in title for word in ["miss", "drop", "loss", "weak"]):
                negative += 1

        if positive > negative:
            return "חיובי"
        elif negative > positive:
            return "שלילי"
        return "ניטרלי"
    except Exception as e:
        print(f"שגיאת סנטימנט עבור {symbol}: {e}")
        return "לא זמין"

