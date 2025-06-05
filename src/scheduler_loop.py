import time
from datetime import datetime, timedelta
import pytz
from market_time_utils import is_real_trading_day, is_no_real_trading, get_market_close_hour
from risk_management import detects_weakness

from messaging import send_macro_event_summary_before, send_macro_event_summary_after, send_no_real_trading_alert, send_final_signal, send_weakness_alert
from macro import get_macro_summary, format_macro_summary
from time_config import START_HOUR, START_MINUTE, END_HOUR, END_MINUTE, MACRO_EVENT_HOUR, MACRO_EVENT_MINUTE

# משתנים גלובליים
sent_today_start = False
sent_today_end = False
last_day = None
sent_macro_before = False
sent_macro_after = False

sent_weakness_alert = False

def daily_schedule_loop():
    global sent_today_start, sent_today_end, last_day
    global sent_macro_before, sent_macro_after

    while True:
        now = datetime.now(pytz.timezone('Asia/Jerusalem'))
        current_hour = now.hour
        current_minute = now.minute

        # הדפסת מצב
        print(
            f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] שעה: {current_hour} | דקה: {current_minute} | התחלה: {sent_today_start} | סיום: {sent_today_end}"
        )

        # איפוס יומי
        if last_day != now.date():
            sent_today_start = False
            sent_today_end = False
            sent_macro_before = False
            sent_macro_after = False
            last_day = now.date()

        # שליחת הודעת התחלה
        if not sent_today_start and current_hour == START_HOUR and current_minute == START_MINUTE:
            print(">>> שליחת הודעת התחלה")
                send_start_message()
            sent_today_start = True

        if is_trading_day() and not is_real_trading_day():
                send_no_real_trading_alert("📢 היום מוגדר כיום מסחר, אך בפועל אין מסחר (חג או אירוע חריג).")

        # שליחת הודעת סיום
        if not sent_today_end and current_hour == END_HOUR and current_minute == END_MINUTE:
            print(">>> שליחת הודעת סיום")
                send_end_message()
            sent_today_end = True

        # שליחת התראת מאקרו שעה לפני
        if not sent_macro_before:
            event_time = now.replace(hour=MACRO_EVENT_HOUR,
                                     minute=MACRO_EVENT_MINUTE,
                                     second=0,
                                     microsecond=0)
            if now >= event_time - timedelta(
                    hours=1) and now < event_time - timedelta(minutes=59):
                print(">>> שליחת התראת מאקרו - שעה לפני")
                summary = get_macro_summary()
                text = format_macro_summary(summary)
                send_macro_event_summary_before(text)
                sent_macro_before = True

        if not sent_weakness_alert and detects_weakness(chosen_symbol):
    ...
    sent_weakness_alert = True

        # שליחת התראת מאקרו רבע שעה אחרי
        if not sent_macro_after:
            event_time = now.replace(hour=MACRO_EVENT_HOUR,
                                     minute=MACRO_EVENT_MINUTE,
                                     second=0,
                                     microsecond=0)
            if now >= event_time + timedelta(
                    minutes=15) and now < event_time + timedelta(minutes=16):
                print(">>> שליחת סיכום מאקרו - רבע שעה אחרי")
                summary = get_macro_summary()
                text = format_macro_summary(summary)
                send_macro_event_summary_after(text)
                sent_macro_after = True

# שליחת האיתות לפי זמן סגירה (רגיל / מקוצר / פערי שעון)
signal_hour = get_market_close_hour() - 1
signal_minute = 40

if now.hour == signal_hour and now.minute == signal_minute:
    if signal_ready:
        # חישובי סיכון-סיכוי
        potential_reward_pct = round(((take_profit - entry_price) / entry_price) * 100, 2)
        potential_risk_pct = round(((entry_price - stop_loss) / entry_price) * 100, 2)
        potential_reward_usd = round(account_size * (potential_reward_pct / 100), 2)
        potential_risk_usd = round(account_size * (potential_risk_pct / 100), 2)

        send_final_signal(
            symbol=chosen_symbol,
            direction=direction,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            order_type=order_type,
            sector=sector,
            daily_trend=daily_trend,
            weekly_trend=weekly_trend,
            monthly_trend=monthly_trend,
            zones=zones,
            fundamental_summary=fundamental_summary,
            future_expectation=future_expectation,
            sp500_trend=sp500_trend,
            nasdaq_trend=nasdaq_trend,
            vix_level=vix_level,
            ai_insight_1=ai_insight_1,
            ai_insight_2=ai_insight_2,
            confidence_level=confidence_level,
            potential_reward_pct=potential_reward_pct,
            potential_reward_usd=potential_reward_usd,
            potential_risk_pct=potential_risk_pct,
            potential_risk_usd=potential_risk_usd
        )
    else:
        reason = analyze_why_no_signal_was_sent()
        send_no_signal_reason(reason)

        time.sleep(60)
