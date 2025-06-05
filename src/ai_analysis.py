def get_ai_insights(symbol, technicals, fundamentals):
    insights = []

    # ודא שהמפתחות קיימים כדי למנוע שגיאות
    try:
        if fundamentals.get("trend") == "צמיחה" and technicals.get("trend") == "bullish":
            insights.append("📈 התאמה חזקה בין ניתוח טכני לצמיחה פונדומנטלית")
        
        if technicals["indicators"].get("rsi", 50) < 35 and technicals["indicators"].get("macd", 0) > 0:
            insights.append("📉 מצב oversold – מומנטום מתחיל להתהפך לחיובי")
        
        if fundamentals.get("fundamental_score", 0) >= 75:
            insights.append("🤖 ציון AI גבוה – החברה מצטיינת במדדים הפונדומנטליים")
    except Exception as e:
        insights.append("⚠️ לא ניתן לחשב תובנות AI – בעיה בנתונים")

    # אם אין תובנות בכלל
    if not insights:
        insights = ["🧠 אין תובנות חזקות כרגע", "📌 המשך ניטור יומי מומלץ"]

    return insights[:2]
