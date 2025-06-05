def get_ai_insights(symbol, technicals, fundamentals):
    insights = []

    # תובנה ראשונה לדוגמה: התאמה בין טכני לפונדומנטלי
    if fundamentals["trend"] == "צמיחה" and technicals["trend"] == "bullish":
        insights.append("⚡️ התאמה חזקה בין ניתוח טכני לצמיחה פונדומנטלית")

    # תובנה שנייה: ניתוח אינדיקטורים
    if technicals["indicators"]["rsi"] < 35 and technicals["indicators"]["macd"] > 0:
        insights.append("📈 תבנית oversold עם איתות חיובי – מומנטום משתנה לטובה")

    # תובנה שלישית לדוגמה (אם יש עוד מקום)
    if fundamentals["fundamental_score"] >= 75:
        insights.append("📊 דירוג AI גבוה – החברה מציגה איתנות גבוהה")

    # אם אין תובנות – תן ברירת מחדל
    if not insights:
        insights = ["🤖 לא זוהו תובנות AI ייחודיות, אך הנתונים תקינים"]

    return insights[:2]  # מחזיר עד 2 תובנות
