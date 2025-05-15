import requests
from config import ALPHA_VANTAGE_API_KEY, NEWS_API_KEY
from utils import log_error

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
            log_error(f"שגיאה בניתוח פונדומנטלי של {symbol}: {str(e)}")
            continue

    return results


def fetch_company_overview(symbol):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if "Symbol" in data:
            return data
    except Exception as e:
        log_error(f"שגיאה בקבלת overview עבור {symbol}: {str(e)}")
    return None


def fetch_news_sentiment(symbol):
    url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}"
    try:
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
        else:
            return "ניטרלי"
    except Exception as e:
        log_error(f"שגיאה בשליפת סנטימנט חדשות עבור {symbol}: {str(e)}")
        return "לא זמין"

