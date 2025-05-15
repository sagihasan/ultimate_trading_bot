def analyze_macro_conditions():
    """
    סימולציה פשוטה – ניתן להרחיב את זה לשליפות אמיתיות ממקורות כמו Investing או FRED.
    """
    # דוגמה של תנאים נוכחיים – יש להחליף בנתונים בזמן אמת
    macro = {
        "gdp_growth": True,
        "interest_rate_stable": True,
        "inflation_under_control": True,
        "unemployment_low": True,
        "event_impact": "בינוני",
        "note": "המאקרו תומך בשוק"
    }

    if not (macro["gdp_growth"] and macro["inflation_under_control"]):
        macro["note"] = "המאקרו מאותת זהירות"
        macro["event_impact"] = "חזק"

    return macro
