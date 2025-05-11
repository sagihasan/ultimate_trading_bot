# trade_manager.py – ניהול עסקאות חכם בזמן אמת

from config import ACCOUNT_SIZE, RISK_PERCENTAGE, DISCORD_PUBLIC_WEBHOOK
from utils import send_discord_message

# ניהול עסקאות פתוחות לפי תנאי שוק בזמן אמת

def manage_open_trades(fundamentals, technicals):
    for stock in technicals:
        symbol = stock["symbol"]
        score = stock.get("score", 0)
        candle = stock.get("candle_reversal")
        reversal_zone = stock.get("reversal_zone")
        pattern_flag = stock.get("pattern_flag_or_triangle")
        trend = stock.get("trend_daily")
        can_leverage = stock.get("can_leverage", False)

        fund = fundamentals.get(symbol, {})
        outlook = fund.get("future_outlook")
        sentiment = fund.get("news_sentiment")
        cap = fund.get("market_cap", 0)

        if score < 50 or outlook != "צמיחה עתידית חזקה" or sentiment != "חיובי" or cap < 2e9:
            continue

        # חישוב כמות לפי סיכון
        price = stock["price"]
        stop_loss = price * (1 - 0.03)
        take_profit = price * (1 + 0.06)
        risk_amount = ACCOUNT_SIZE * RISK_PERCENTAGE
        qty = int(risk_amount / (price - stop_loss))

        # הודעת איתות קרבית
        message = (
            f"איתות לכניסה – לונג\n"
            f"סימול: {symbol}\n"
            f"פקודת כניסה: Stop Limit\n"
            f"מחיר כניסה מתוכנן: {round(price, 2)}\n"
            f"סטופ לוס: {round(stop_loss, 2)}\n"
            f"טייק פרופיט: {round(take_profit, 2)}\n"
            f"כמות מניות: {qty}\n"
            f"צפי עתידי: {fund.get('future_event_note', '')}\n"
            f"מגמות: יומי: {stock['trend_daily']} | שבועי: {stock['trend_weekly']} | חודשי: {stock['trend_monthly']}\n"
            + (f"נר היפוך מזוהה: {candle}\n" if candle else "")
            + ("נמצאת באזור פסגות/תחתיות\n" if reversal_zone else "")
            + ("נמצאת בתבנית דגל/משולש\n" if pattern_flag else "") +
            f"מינוף: {'כן' if can_leverage else 'לא'}\n"
            f"הבוט קובע: להיכנס לעסקה\n"
            f"יחס סיכוי-סיכון: 1:2\n"
            f"סיכון לעסקה: {round(risk_amount, 2)}$ ({int(RISK_PERCENTAGE * 100)}%)"
        )

        send_discord_message(DISCORD_PUBLIC_WEBHOOK, message)
