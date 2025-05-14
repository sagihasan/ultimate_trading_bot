# macro.py — סיכום שבועי כולל סקטורים ואירועים

from fundamentals import analyze_fundamentals
from technicals import run_technical_analysis
from stock_list import STOCK_LIST
from utils import send_discord_message
from config import DISCORD_PUBLIC_WEBHOOK_URL
from collections import defaultdict
from datetime import datetime

# 12:00 ב־ראשון בכל שבוע הודעת סיכום מאקרו
def send_macro_summary():
    fundamentals = analyze_fundamentals(STOCK_LIST)
    technicals = run_technical_analysis(STOCK_LIST)

    # דירוג סקטור ודירוג ממוצע ניקוד טכני
    sector_scores = defaultdict(list)
    for stock in technicals:
        symbol = stock["symbol"]
        score = stock.get("score", 0)
        sector = fundamentals.get(symbol, {}).get("sector", "ללא סקטור")
        if score:
            sector_scores[sector].append(score)

    sector_avg = {k: round(sum(v)/len(v), 2) for k, v in sector_scores.items()}
    sorted_sectors = sorted(sector_avg.items(), key=lambda x: x[1], reverse=True)

    best_sector_last_week = sorted_sectors[0][0] if sorted_sectors else "לא זמין"
    predicted_best_sector = sorted_sectors[1][0] if len(sorted_sectors) > 1 else best_sector_last_week

    message = (
        "**סקירה שבועית — מאקרו**\n\n"
        f"• הסקטור שהוביל בשבוע האחרון: **{best_sector_last_week}**\n"
        f"• התחזית לשבוע הבא: **{predicted_best_sector}**\n\n"
        "• נתוני מאקרו צפויים:\n"
        "- נאום פאוול, ריבית ארה\"ב, CPI, אבטלה ועוד\n"
        "- הבוט יעדכן אם תהיה השפעה צפויה על שוק או מניות\n\n"
        "בהצלחה לשבוע הקרוב!"
    )

    send_discord_message(DISCORD_PUBLIC_WEBHOOK, message)

