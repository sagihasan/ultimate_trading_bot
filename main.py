import os
import time
from datetime import datetime
from dotenv import load_dotenv
from discord_test import send_discord_message, public_webhook
from fundamentals import analyze_fundamentals
from technicals import analyze_technicals

load_dotenv()

def main_trading_bot():
    print("הבוט התחיל לפעול ✅")

    while True:
        current_time = datetime.now().strftime('%H:%M')
        
        # דוגמה לשעות של איתות יומי
        if current_time == '21:40':
            fundamentals_result = analyze_fundamentals()
            technicals_result = analyze_technicals()

            if fundamentals_result['status'] and technicals_result['status']:
                signal_message = f"""
📈 איתות יומי:

סוג עסקה: {technicals_result['signal_type']}
מחיר כניסה: {technicals_result['entry_price']}
סטופ לוס: {technicals_result['stop_loss']}
טייק פרופיט: {technicals_result['take_profit']}

צפי עתידי של החברה: {fundamentals_result['future_outlook']}
הבוט קובע: {technicals_result['final_decision']}
"""
                send_discord_message(public_webhook, signal_message)
            else:
                send_discord_message(public_webhook, "היום אין איתות עקב שוק תנודתי או נתונים חסרים.")

            time.sleep(60)  # המתנה של דקה כדי לא לשלוח שוב באותה דקה

        # כאן אפשר להוסיף עוד בדיקות כמו דוחות שבועיים / חודשי וכו'

        time.sleep(10)

if __name__ == '__main__':
    main_trading_bot()
