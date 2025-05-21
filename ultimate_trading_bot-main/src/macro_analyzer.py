# macro_analyzer.py

def analyze_macro_trends(macro_summary):
    """
    מחזיר מגמה כוללת של שוק המניות לפי נתוני המאקרו
    """
    sp_trend = macro_summary["sp500"]["daily"]
    nasdaq_trend = macro_summary["nasdaq"]["daily"]
    vix_trend = macro_summary["vix_trend"]["daily"]

    if sp_trend == "עלייה" and nasdaq_trend == "עלייה" and vix_trend == "ירידה":
        return "שוק שורי"
    elif sp_trend == "ירידה" and nasdaq_trend == "ירידה" and vix_trend == "עלייה":
        return "שוק דובי"
    else:
        return "שוק מעורב"

def analyze_macro_calendar():
    # לוגיקה לניתוח לוח מאקרו
    return "ניתוח מאקרו בוצע"

def format_macro_summary(macro_summary):
    """
    פורמט יפה להצגת סיכום מאקרו בדיסקורד
    """
    return (
        f"**S&P 500**: יומי – {macro_summary['sp500']['daily']} | "
        f"שבועי – {macro_summary['sp500']['weekly']} | "
        f"חודשי – {macro_summary['sp500']['monthly']}\n"
        f"**Nasdaq**: יומי – {macro_summary['nasdaq']['daily']} | "
        f"שבועי – {macro_summary['nasdaq']['weekly']} | "
        f"חודשי – {macro_summary['nasdaq']['monthly']}\n"
        f"**P/E**: {macro_summary['pe_ratio']}\n"
        f"**VIX**: יומי – {macro_summary['vix_trend']['daily']}, "
        f"שבועי – {macro_summary['vix_trend']['weekly']}, "
        f"חודשי – {macro_summary['vix_trend']['monthly']}"
    )


def detect_gap_warning_from_macro(macro_summary):
    """
    התראה אם צפוי גאפ חזק הפוך למגמת עסקה פתוחה
    """
    vix_trend = macro_summary["vix_trend"]["daily"]
    sp_trend = macro_summary["sp500"]["daily"]

    if vix_trend == "עלייה" and sp_trend == "ירידה":
        return "יתכן גאפ שלילי חזק – שים לב אם יש עסקת לונג פתוחה"
    elif vix_trend == "עלייה" and sp_trend == "עלייה":
        return "ויקס עולה למרות מגמה חיובית – שים לב לגאפ הפוך"
    return None


def detect_upcoming_crisis(macro_summary):
    """
    התרעה אם זוהו תנאים שמצביעים על משבר כלכלי מתקרב
    """
    if (
        macro_summary["sp500"]["daily"] == "ירידה"
        and macro_summary["nasdaq"]["daily"] == "ירידה"
        and macro_summary["vix_trend"]["daily"] == "עלייה"
        and macro_summary["pe_ratio"] != "לא זמין"
        and macro_summary["pe_ratio"] > 22
    ):
        return "התרעת משבר אפשרי: מגמת ירידה + מדד פחד עולה + מכפיל גבוה"
    return None
