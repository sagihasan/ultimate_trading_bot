# macro_analyzer.py

from macro import (
    get_macro_data,
    detect_upcoming_crisis,
    detect_gap_warning_from_macro,
    format_macro_summary,
    is_market_bullish
)

def analyze_macro():
    events = get_macro_data()
    summary = format_macro_summary()
    bullish = is_market_bullish(summary)

    alerts = []

    # בדיקת גאפ צפוי מאירוע מקרו
    gap_alert = detect_gap_warning_from_macro(events)
    if gap_alert:
        alerts.append(gap_alert)

    # בדיקת משבר פוטנציאלי
    crisis_alert = detect_upcoming_crisis(events)
    if crisis_alert:
        alerts.append(crisis_alert)

    # מצב השוק הכללי
    market_trend = "Bullish (עולה)" if bullish else "Bearish (יורד)"

    report = f"""**סקירה מקרו לשוק**
{summary}

**מצב השוק הכללי:** {market_trend}
"""
    if alerts:
        report += "\n\n**התראות חשובות:**\n" + "\n".join(alerts)

    return report
