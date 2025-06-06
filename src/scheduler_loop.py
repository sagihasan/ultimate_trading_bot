import time
from datetime import datetime, timedelta
import pytz
from market_time_utils import is_real_trading_day, is_no_real_trading, get_market_close_hour
from risk_management import detects_weakness, detect_bubble_conditions
from risk_management import detect_bubble_conditions, detect_crisis, detect_institutional_activity, detect_emergency_crash, summarize_open_trades
from fundamentals import get_sp500_pe_ratio, get_fundamental_summary
from technicals import detect_volume_surge, get_signal_direction, get_technicals_summary, calculate_fibonacci_levels, get_current_price
from market_analysis import get_sp500_trend, get_nasdaq_trend, get_vix_level
from risk_management import open_position, close_position
from ai_analysis import get_ai_insights

from messaging import send_macro_event_summary_before, send_macro_event_summary_after, send_no_real_trading_alert, send_final_signal, send_weakness_alert, send_bubble_alert, send_crisis_alert, send_gap_alert, send_gap_exit_alert, send_intraday_weakness_alert, detect_premarket_weakness, detect_live_weakness, detect_aftermarket_weakness, send_gap_forecast_alert, detect_institutional_activity_alert, send_fibonacci_alert, send_trend_conflict_alert, send_emergency_crash_alert, classify_pe_ratio, classify_vix, send_nightly_market_summary, send_weekly_private_morning, send_weekly_macro_outlook
from macro import get_macro_summary, format_macro_summary
from time_config import START_HOUR, START_MINUTE, END_HOUR, END_MINUTE, MACRO_EVENT_HOUR, MACRO_EVENT_MINUTE
from gap_analysis import detect_expected_gap, predict_gap
from position_utils import check_open_position, get_position_direction
from strategic_zones import check_strategic_zones

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

        is_sunday = weekday == 6

    if now_str == "11:30" and is_sunday:
        send_weekly_private_morning()

        if now_str == "12:00" and is_sunday:
    macro_events = get_upcoming_macro_events()  # זו פונקציה שצריכה להביא את האירועים הקרובים
    send_weekly_macro_outlook(macro_events)

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

for symbol in stock_list:

position_direction = get_signal_direction(symbol)
if open_position and detect_emergency_crash(symbol):
    reason = "נר אדום עצום, ווליום קיצוני וחדירה מתחת לכל רמות התמיכה"
    direction = position_direction  # לונג או שורט
    send_emergency_crash_alert(symbol, reason, direction)
    close_position(symbol)
    
if daily_trend != weekly_trend:
    send_trend_conflict_alert(symbol, daily_trend, weekly_trend)
    
if open_position:
    fib_levels = calculate_fibonacci_levels(symbol)
    current_price = get_current_price(symbol)

    if fib_levels:
        for level_name, level_price in fib_levels.items():
            distance = abs(current_price - level_price) / current_price

            if distance < 0.01:  # פחות מ־1% מהמחיר הנוכחי
                suggestion = "עדכן סטופ לוס או סגור חלקית – קרוב לרמת פיבונאצ’י משמעותית"
                send_fibonacci_alert(symbol, level_name, level_price, current_price, suggestion)
                break
                
data = get_recent_candles(symbol)
zones = check_strategic_zones(symbol, data)

zones_description = " | ".join(zones) if zones else "לא נמצאו אזורים מיוחדים"

# אם יש אזור חשוב – שלח התראה
if zones:
    zone_message = (
        f"🧭 **זוהה אזור אסטרטגי למניה {symbol}**\n"
        f"📌 אזור(ים): {zones_description}\n"
        f"⚠️ ייתכן שינוי מגמה – עקוב מקרוב!"
    )
    send_message(DISCORD_PUBLIC_WEBHOOK_URL, zone_message)
    
institutional_activity = detect_institutional_activity(symbol)
if institutional_activity:
    send_institutional_activity_alert(
        symbol,
        institutional_activity["type"],
        institutional_activity["volume"],
        institutional_activity["body"]
    )
    
gap_info = predict_gap(symbol)

if open_position and gap_info and gap_info["expected"]:
    if (position_direction == "לונג" and "למטה" in gap_info["direction"]) or \
       (position_direction == "שורט" and "למעלה" in gap_info["direction"]):
        
        send_gap_exit_alert(
            symbol,
            gap_info["gap_pct"],
            gap_info["direction"],
            gap_info["strength"],
            position_direction
        )
           
gap_data = predict_gap(symbol)
if gap_data and gap_data["expected"]:
    send_gap_forecast_alert(
        symbol=symbol,
        expected_gap_pct=gap_data["gap_pct"],
        direction=gap_data["direction"],
        strength=gap_data["strength"],
        position_direction=direction if open_position else None
    )
    
    if is_position_open(symbol):  # בדיקת עסקה פתוחה למניה
        # 🔎 חולשה בפרי־מרקט
        if detect_premarket_weakness(symbol):
            send_intraday_weakness_alert(
                symbol=symbol,
                market_phase="פרי־מרקט",
                weakness_type="נפח נמוך וירידות מתמשכות לפני פתיחה",
                action="צא מיידית או עדכן סטופ – לפני שהנפילה תתחיל באמת"
            )

        # 🔎 חולשה בזמן המסחר
        if detect_live_weakness(symbol):
            send_intraday_weakness_alert(
                symbol=symbol,
                market_phase="שעות מסחר",
                weakness_type="נרות אדומים רצופים עם ווליום עולה",
                action="הוראה קרבית: סגור חצי מהעסקה או עדכן סטופ – תוקפים לפני שהשוק יתקוף"
            )

        # 🔎 חולשה באפטר־מרקט
        if detect_aftermarket_weakness(symbol):
            send_intraday_weakness_alert(
                symbol=symbol,
                market_phase="אפטר־מרקט",
                weakness_type="מכירת סוף יום עם המשך ירידות",
                action="חולשה חמורה – הכן יציאה עוד הלילה או בפתיחה הקרובה"
            )
        close_position(symbol)  # אפשרי אם אתה רוצה שהבוט יסגור לבד עסקאות על חולשה
        
    # בדיקה אם קיימת עסקה פתוחה
open_position = check_open_position(symbol)
if open_position:
    position_direction = get_position_direction(symbol)
else:
    position_direction = None

# התראת יציאה אם יש גאפ נגד הכיוון של העסקה
if open_position and gap_info:
    if (position_direction == "לונג" and "למטה" in gap_info["direction"]) or \
       (position_direction == "שורט" and "למעלה" in gap_info["direction"]):

        send_gap_exit_alert(
            symbol,
            gap_info["gap_pct"],
            gap_info["direction"],
            gap_info["strength"],
            position_direction
        )
    
    gap_info = detect_expected_gap(symbol)
if gap_info:
    send_gap_alert(symbol, gap_info)

    if open_position and gap_info:
    if (position_direction == "לונג" and "למטה" in gap_info["direction"]) or \
       (position_direction == "שורט" and "למעלה" in gap_info["direction"]):
        
        send_gap_exit_alert(
            symbol,
            gap_info["gap_pct"],
            gap_info["direction"],
            gap_info["strength"],
            position_direction
        )

         close_position(symbol)
    
    crisis_detected, direction, indicators_summary = detect_crisis(symbol)

if crisis_detected:
    send_crisis_alert(
        symbol=symbol,
        direction=direction,
        indicators_summary=indicators_summary,
        has_open_position=open_position,
        current_position_direction=direction
    )
    ...
    # קבלת נתוני שוק כלליים
    sp500_trend = get_sp500_trend()
    nasdaq_trend = get_nasdaq_trend()
    vix_level = get_vix_level()
    pe_ratio = get_sp500_pe_ratio()
    volume_surge = detect_volume_surge(symbol)
    direction = get_signal_direction(symbol)  # לונג או שורט
    
reason = (
    f"השוק מראה סימנים מובהקים לבועה כלפי {bubble_direction}:\n"
    f"• S&P 500: {sp500_trend}\n"
    f"• Nasdaq: {nasdaq_trend}\n"
    f"• VIX: {vix_level}\n"
    f"• מכפיל רווח: {pe_ratio}\n"
    f"• נפח מסחר חריג: {'כן' if volume_surge else 'לא'}"
)

suggestion = "רמת סיכון מוגברת – עדכן סטופ לוס, צמצם פוזיציה או הימנע מכניסה. אין רחמים בשוק בועה!"

send_bubble_alert(reason, suggestion)

    ...

ai_insights = get_ai_insights(symbol, technicals, fundamentals)
ai_insight_1 = ai_insights[0]
ai_insight_2 = ai_insights[1]

    # המשך ניתוח טכני ופונדומנטלי
    ...

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
        open_position(chosen_symbol)

        now_str = datetime.now().strftime("%H:%M")

if now_str == "02:00":
    nasdaq_change = get_nasdaq_daily_change()
    sp500_change = get_sp500_daily_change()
    pe_ratio = get_sp500_pe_ratio()
    vix_value = get_vix_value()
    open_trades_summary = summarize_open_trades()

    send_nightly_market_summary(nasdaq_change, sp500_change, pe_ratio, vix_value, open_trades_summary)

        time.sleep(60)
