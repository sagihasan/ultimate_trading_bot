from datetime import datetime, timedelta

def get_upcoming_macro_events():
    # כאן אפשר להחליף לאירועים אמיתיים אם תחבר API כמו Investing או TradingEconomics
    today = datetime.now()
    events = [
        {"date": (today + timedelta(days=0)).strftime("%A %d/%m"), "title": "נאום יו\"ר הפד", "impact": "🔴 חזק"},
        {"date": (today + timedelta(days=1)).strftime("%A %d/%m"), "title": "מדד מחירים לצרכן (CPI)", "impact": "🟠 בינוני"},
        {"date": (today + timedelta(days=2)).strftime("%A %d/%m"), "title": "מדד מנהלי רכש (PMI)", "impact": "🟡 קל"},
        {"date": (today + timedelta(days=4)).strftime("%A %d/%m"), "title": "נתוני אבטלה", "impact": "🔴 חזק"},
        {"date": (today + timedelta(days=5)).strftime("%A %d/%m"), "title": "תמ\"ג רבעוני", "impact": "🟠 בינוני"},
    ]
    return events
