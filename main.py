import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from utils import send_discord_message
from fundamentals import analyze_fundamentals
from technicals import run_technical_analysis
from config import ACCOUNT_SIZE, RISK_PERCENTAGE, STOP_LOSS_PERCENT, TAKE_PROFIT_PERCENT
import exchange_calendars as ec

# טען את ה-Webhookים מהסביבה
private_webhook = os.getenv('DISCORD_PRIVATE_WEBHOOK')
public_webhook = os.getenv('DISCORD_PUBLIC_WEBHOOK')
error_webhook = os.getenv('DISCORD_ERROR_WEBHOOK')

load_dotenv()

# הגדר את הבורסה של NYSE
nyse = ec.get_calendar("XNYS")

def get_market_info(date):
    session = nyse.sessions_in_range(date, date)
    if not session.empty:
        if nyse.is_session(date):
            close_time = nyse.session_close(date).tz_convert('Israel')
            open_time = nyse.session_open(date).tz_convert('Israel')
            duration = (close_time - open_time).total_seconds() / 3600
            if duration < 6:  # חצי יום
                return "half_day", close_time
            else:
                return "full_day", close_time
    else:
        holiday = nyse.holidays().holidays
        reason = None
        if date in holiday:
            reason = "חג רשמי בארה״ב"
        else:
            reason = "יום לא מסחר"
        return "no_trading", reason

def is_dst_gap():
    today = datetime.now()
    march = datetime(today.year, 3, 8)
    november = datetime(today.year, 11, 1)
    dst_start = march + timedelta(days=(6 - march.weekday()))
    dst_end = november + timedelta(days=(6 - november.weekday()))
    return dst_start <= today <= dst_end

def main_trading_bot():
    try:
        print("הבוט התחיל לפעול ✅")

        while True:
            now = datetime.now()
            current_time = now.strftime('%H:%M')
            today_date = now.normalize()

            # פתיחה - 11:00
            if current_time == '11:00':
                send_discord_message(private_webhook, "🤖 הבוט התחיל לפעול ✅")
                send_discord_message(private_webhook, "📢 תזכורת: שבוע חדש – תעיין בכל העדכונים בערוץ הציבורי!")
                time.sleep(60)

            # סגירה - 02:10
            if current_time == '02:10':
                send_discord_message(private_webhook, "🤖 הבוט סיים לפעול 🛑")
                time.sleep(60)

            # בדיקה איזה סוג יום זה
            market_status, info = get_market_info(today_date)

            # קובע את שעת האיתות לפי סוג היום
            signal_time = None
            if market_status == "full_day":
                signal_time = "21:40" if is_dst_gap() else "22:40"
            elif market_status == "half_day":
                close_time = info - timedelta(minutes=20)
                signal_time = close_time.strftime('%H:%M')
            elif market_status == "no_trading":
                if current_time == '11:10':
                    send_discord_message(public_webhook, f"📢 היום אין מסחר בארה\"ב ({info}) – לא יישלח איתות.")
                    time.sleep(60)

            # איתות יומי בשעה הנכונה
            if signal_time and current_time == signal_time:
                fundamentals_result = analyze_fundamentals()
                technicals_result_list = run_technical_analysis()

                for technicals_result in technicals_result_list:
                    if technicals_result['MA_Cross_Long'] and technicals_result['MACD_Bullish']:
                        price = technicals_result['price']
                        stop_loss_price = price * (1 - STOP_LOSS_PERCENT)
                        take_profit_price = price * (1 + TAKE_PROFIT_PERCENT)

                        risk_amount = ACCOUNT_SIZE * RISK_PERCENTAGE
                        per_share_risk = price - stop_loss_price
                        quantity = int(risk_amount / per_share_risk) if per_share_risk > 0 else 0

                        signal_message = f"""
📈 איתות יומי:

מניה: {technicals_result['symbol']}
סוג עסקה: לונג
מחיר כניסה: {price:.2f}
סטופ לוס: {stop_loss_price:.2f}
טייק פרופיט: {take_profit_price:.2f}
כמות מניות: {quantity} מניות

💰 ניהול סיכונים:
סיכון מקסימלי לעסקה: {risk_amount:.2f}$
סיכון פר מניה: {per_share_risk:.2f}$
סה"כ סיכון בפועל: {(quantity * per_share_risk):.2f}$

צפי עתידי של החברה: {fundamentals_result['future_outlook']}
הבוט קובע: להיכנס לעסקה ✅
"""
                        send_discord_message(public_webhook, signal_message)
                        break
                else:
                    send_discord_message(public_webhook, "📉 היום אין איתות עקב שוק תנודתי או נתונים חסרים.")
                time.sleep(60)

            time.sleep(10)

    except Exception as e:
        error_message = f"❌ שגיאה בבוט: {str(e)}"
        send_discord_message(error_webhook, error_message)
        print(error_message)

if __name__ == '__main__':
    main_trading_bot()
