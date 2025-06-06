# macro_analysis.py

from indices import get_index_change
from risk_management import suggest_new_stop_price
from messaging import send_message, DISCORD_PUBLIC_WEBHOOK_URL

def analyze_market_reaction(event):
    """
    מזהה את השפעת האירוע על השוק – התרסקות, חולשה, עוצמה או ללא תגובה.
    """
    sp500_change = get_index_change("S&P 500")
    nasdaq_change = get_index_change("NASDAQ")

    avg_change = (sp500_change + nasdaq_change) / 2

    if avg_change <= -1.5:
        return "crash"
    elif -1.5 < avg_change <= -0.5:
        return "weakness"
    elif avg_change >= 1.0:
        return "strength"
    else:
        return "none"

def suggest_new_stop_price(symbol, direction):
    """
    מייצר מחיר סטופ חדש לפי כיוון העסקה.
    לדוגמה – אם לונג: מעלה את הסטופ, אם שורט: מוריד.
    """
    current_price = get_current_price(symbol)

    if direction == "long":
        return round(current_price * 0.98, 2)  # עדכון סטופ לוס 2% מתחת
    elif direction == "short":
        return round(current_price * 1.02, 2)  # עדכון סטופ לוס 2% מעל
    else:
        return current_price

# ודא שיש לך את הפונקציה get_current_price בקובץ data_utils או במקור אחר
from data_utils import get_current_price
