# import os
import requests
from config import ALPHA_VANTAGE_API_KEY, NEWS_API_KEY

# ניתוח פונדומנטלי של מניות

def analyze_fundamentals(symbols):
    results = {}
    for symbol in symbols:
        try:
            overview = get_company_overview(symbol)
            sentiment = get_news_sentiment(symbol)

            market_cap = float(overview.get("MarketCapitalization", 0))
            revenue = float(overview.get("RevenueTTM", 0))
            net_income = float(overview.get("NetIncomeTTM", 0))
            sector = overview.get("Sector", "Unknown")
            future = sentiment.get("summary", "לא ידוע")

            status = "נפילה" if net_income < 0 else ("צמיחה" if net_income > 0 else "נייטרלי")

            results[symbol] = {
                "symbol": symbol,
                "market_cap": market_cap,
                "revenue": revenue,
                "net_income": net_income,
                "sector": sector,
                "status": status,
                "future_outlook": future
            }
        except Exception as e:
            print(f"שגיאה בנתונים פונדומנטליים של {symbol}: {e}")
            continue

    return results


def get_company_overview(symbol):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    return response.json()


def get_news_sentiment(symbol):
    url = f"https://newsapi.org/v2/everything?q={symbol}&language=en&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    summary = "חיובי" if len(articles) >= 3 else "נייטרלי"
    return {"summary": summary, "articles": articles[:3]}

