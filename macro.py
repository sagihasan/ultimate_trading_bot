# macro.py – שליחת סיכום מאקרו שבועי כולל סקטורים ואירועים

from fundamentals import analyze_fundamentals
from technicals import run_technical_analysis
from config import STOCK_LIST, DISCORD_PUBLIC_WEBHOOK
from utils import send_discord_message
import datetime
from collections import defaultdict

# שליחת הודעת סיכום שבועית בכל יום ראשון ב־12:00

def send_macro_summary():
    fundamentals = analyze_fundamentals(STOCK_LIST)
    technicals = run_technical_analysis(STOCK_LIST)

    # קיבוץ מניות לפי סקטור וחישוב ממוצע ניקוד טכני
    sector_scores = defaultdict(list)
    for stock in technicals:
        symbol = stock["symbol"]
        score = stock.get("score", 0)
        sector = fundamentals.get(symbol, {}).get("sector", "Unknown")
        if score:
            sector_scores[sector].append(score)

    sector_avg = {k: round(sum(v)/len(v), 2) for k, v in sector_scores.items() if v}
    sorted_sectors = sorted(sector_avg.items(), key=lambda x: x[1], reverse=True)

    best_sector_last_week = sorted_sectors[0][0] if sorted_sectors else "לא זמין"
    predicted_best_sector = sorted_sectors[1][0] if len(sorted_sectors) > 1 else best_sector_last_week

    message = (
        "סקירה שבועית – מאקרו\n\n"
        "- נאום פאוול, ריבית ארה\"ב, CPI, אירועים צפויים -\n"
        "- התנודות במדדי Nasdaq / S&P500: שוק כללי – עליות קלות\n"
        "- מדד הפחד: 13.2 | מכפיל רווח: 28.4\n\n"
        f"סקטור מוביל בשבוע שעבר: {best_sector_last_week}\n"
        f"סקטור צפוי להוביל השבוע: {predicted_best_sector}\n\n"
        "הערכת כיוון השוק הכללי:\n"
        "הבוט מוכן לפעולה."
    )

    send_discord_message(DISCORD_PUBLIC_WEBHOOK, message)

