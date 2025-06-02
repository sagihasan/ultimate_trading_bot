import requests
import random


# גרסה פשוטה – ניתוח סנטימנט כללי
def get_general_market_sentiment():
    try:
        news = [
            "the market is crashing", "interest rate hike announced",
            "strong earnings report", "tech stocks rallying"
        ]

        sentiment_score = 0
        for headline in news:
            if "crash" in headline or "hike" in headline:
                sentiment_score -= 1
            elif "strong" in headline or "rally" in headline:
                sentiment_score += 1

        if sentiment_score > 0:
            return "חיובי"
        elif sentiment_score < 0:
            return "שלילי"
        else:
            return "ניטרלי"
    except Exception as e:
        print(f"שגיאה בניתוח סנטימנט כללי: {e}")
        return "לא זמין"


# גרסה לפי מניה (מקבל ticker ומחזיר label ו-score)
def get_market_sentiment(ticker):
    try:
        sentiment_score = round(random.uniform(-1, 1), 2)

        if sentiment_score > 0.3:
            sentiment_label = "חיובי"
        elif sentiment_score < -0.3:
            sentiment_label = "שלילי"
        else:
            sentiment_label = "ניטרלי"

        print(
            f"📊 סנטימנט עבור {ticker}: {sentiment_label} ({sentiment_score})")

        return {
            "sentiment_score": sentiment_score,
            "sentiment_label": sentiment_label
        }

    except Exception as e:
        print(f"שגיאה בניתוח סנטימנט עבור {ticker}: {e}")
        return {"sentiment_score": 0, "sentiment_label": "לא זמין"}
