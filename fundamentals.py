# fundamentals.py – ניתוח פונדומנטלי כולל צפי עתידי, שווי שוק, דוחות ותחזיות

import yfinance as yf
from config import ALPHA_VANTAGE_API_KEY, NEWS_API_KEY
from utils import safe_get

# פונקציה שמחזירה ניתוח פונדומנטלי לכל מניה

def analyze_fundamentals(symbols):
    analysis = {}
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            market_cap = info.get("marketCap", 0)
            revenue = info.get("totalRevenue", 0)
            net_income = info.get("netIncomeToCommon", 0)
            eps = info.get("trailingEps", 0)
            forward_eps = info.get("forwardEps", 0)
            sector = info.get("sector", "Unknown")

            # קביעת תחזית עתידית לפי forward EPS
            if forward_eps and eps:
                future_outlook = "צמיחה עתידית חזקה" if forward_eps > eps else "תחזית חלשה"
            else:
                future_outlook = "תחזית לא זמינה"

            # טקסט מותאם אישית לכל מניה (דוגמה אוטומטית)
            future_event_note = f"צפי להמשך פעילות בתחום {sector} והשקות עתידיות ברבעון הקרוב" if sector != "Unknown" else None

            # סנטימנט חדשותי מ-NewsAPI
            news_url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}&language=en&pageSize=5"
            news_response = safe_get(news_url)

            if news_response and news_response.status_code == 200:
                news_data = news_response.json()
                titles = " ".join([article["title"] for article in news_data.get("articles", [])])
                if any(keyword in titles.lower() for keyword in ["beats expectations", "record profit", "growth"]):
                    sentiment = "חיובי"
                elif any(keyword in titles.lower() for keyword in ["missed", "cut forecast", "loss"]):
                    sentiment = "שלילי"
                else:
                    sentiment = "ניטרלי"
            else:
                sentiment = "לא זמין"

            analysis[symbol] = {
                "symbol": symbol,
                "market_cap": market_cap,
                "revenue": revenue,
                "net_income": net_income,
                "eps": eps,
                "forward_eps": forward_eps,
                "future_outlook": future_outlook,
                "future_event_note": future_event_note,
                "sector": sector,
                "news_sentiment": sentiment
            }
        except Exception as e:
            analysis[symbol] = {"error": str(e)}
    return analysis

