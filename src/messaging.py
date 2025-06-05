import os
import requests

from env_loader import (DISCORD_PUBLIC_WEBHOOK_URL,
                        DISCORD_PRIVATE_WEBHOOK_URL,
                        DISCORD_ERRORS_WEBHOOK_URL)


def send_message(webhook_url, content):
    try:
        data = {"content": content}
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
    except Exception as e:
        print(f"שגיאה בשליחת הודעה לדיסקורד: {e}")


def send_public_message(content):
    send_message(DISCORD_PUBLIC_WEBHOOK_URL, content)


def send_private_message(content):
    send_message(DISCORD_PRIVATE_WEBHOOK_URL, content)


def send_error_message(content):
    send_message(DISCORD_ERRORS_WEBHOOK_URL, content)

def send_macro_event_summary_before(text):
    print(f"📢 תזכורת לאירוע מקרו חזק ({strength}) בעוד שעה ב־{time}: {event}")
    # כאן אפשר להוסיף שליחה לדיסקורד
   send_message(DISCORD_PUBLIC_WEBHOOK_URLׁׁׁׁׁׂ, text)

def send_macro_event_summary_after(text):
    print(f"📢 סיכום לאחר האירוע {event}: {summary}")
    # כאן אפשר להוסיף שליחה לדיסקורד
    send_message(DISCORD_PUBLIC_WEBHOOK_URLׁׁׁׁׁׂ, text)

def send_start_message():
    send_message(DISCORD_PRIVATE_WEBHOOK_URL, "🟢 הבוט התחיל לפעול.")

def send_end_message():
    send_message(DISCORD_PRIVATE_WEBHOOK_URL, "🌙 הבוט סיים לפעול.")

def send_no_signal_reason(reason):
    message = f"❌ לא נשלח איתות היום. הסיבה: {reason}\nהבוט קובע – אין כניסה היום."
    send_message(DISCORD_PUBLIC_WEBHOOK_URL, message)

def send_no_real_trading_alert():
    message = "📛 יום מסחר היום – אך אין מסחר בפועל (כנראה חג בארה\"ב)."
    send_message(DISCORD_PUBLIC_WEBHOOK_URL, message)

def send_final_signal(symbol, direction, entry_price, stop_loss, take_profit, order_type, sector,
                      daily_trend, weekly_trend, monthly_trend, zones, fundamental_summary,
                      sp500_trend, nasdaq_trend, vix_level, ai_insight_1, ai_insight_2,
                      future_expectation,
                      confidence_level, potential_reward_pct, potential_reward_usd,
                      potential_risk_pct, potential_risk_usd):
    message = (
        f"📣 **איתות קרבי – הבוט קובע!**\n"
        f"📌 מניה: **{symbol}**\n"
        f"📈 כיוון העסקה: **{direction}**\n"
        f"💰 סוג פקודה: {order_type}\n"
        f"🎯 מחיר כניסה: {entry_price}\n"
        f"🛑 סטופ לוס: {stop_loss}\n"
        f"🏆 טייק פרופיט: {take_profit}\n"
        f"🏭 סקטור: {sector}\n"
        f"📊 מגמה יומית: {daily_trend}\n"
        f"📈 מגמה שבועית: {weekly_trend}\n"
        f"📅 מגמה חודשית: {monthly_trend}\n"
        f"🧭 אזורים אסטרטגיים: {zones}\n"
        f"📑 ניתוח פונדומנטלי: {fundamental_summary}\n"
        f"🔮 צפי רבעוני של החברה: {future_expectation}\n"
        f"📈 מצב השוק הכללי:\n"
        f"• S&P 500: {sp500_trend}\n"
        f"• Nasdaq: {nasdaq_trend}\n"
        f"• VIX: {vix_level}\n"
        f"🤖 תובנות AI:\n"
        f"• {ai_insight_1}\n"
        f"• {ai_insight_2}\n"
        f"🔐 **רמת ביטחון:** {confidence_level}%\n"
        f"📈 **סיכוי לרווח:** {potential_reward_pct}% | ~{potential_reward_usd}$\n"
        f"⚠️ **סיכון:** {potential_risk_pct}% | ~{potential_risk_usd}$"
    )
    send_message(DISCORD_PUBLIC_WEBHOOK_URL, message)

def send_weakness_alert(symbol, reason, suggestion):
    message = (
        f"⚠️ **סימני חולשה בעסקה פתוחה**\n"
        f"🔍 מניה: {symbol}\n"
        f"📉 סיבה: {reason}\n"
        f"📌 המלצת הבוט: {suggestion}"
    )
    send_message(DISCORD_PUBLIC_WEBHOOK_URL, message)

def send_bubble_alert(reason, suggestion):
    message = (
        f"💥 **התראת בועה!**\n"
        f"📉 {reason}\n"
        f"🛑 **הוראה מהבוט:** {suggestion}\n"
        f"⚠️ שים לב – השוק מראה סימני ניפוח מסוכן, יתכן תיקון חד בקרוב."
    )
    send_message(DISCORD_PUBLIC_WEBHOOK_URL, message)

def send_crisis_alert(symbol, direction, indicators_summary, has_open_position=False, current_position_direction=None):
    base_message = (
        f"🚨 **התראת משבר – סימנים חזקים לתנועה קיצונית צפויה!**\n"
        f"📌 מניה: **{symbol}**\n"
        f"📈 כיוון מוערך: {direction}\n"
        f"📊 אינדיקטורים שמעידים על המשבר:\n{indicators_summary}\n"
    )

    action_message = ""
    if has_open_position:
        if direction != current_position_direction:
            action_message = (
                "⚔️ **הוראה מיידית:** כיוון הפוך לעסקה – צא מיידית או עדכן סטופ!"
            )
        else:
            action_message = (
                "✅ הכיוון תואם – המשך לעקוב, יתכנו תנודות חדות."
            )
    else:
        action_message = (
            "🚫 אין עסקה פתוחה – הימנע מכניסה עד שהתמונה תתבהר!"
        )

    full_message = base_message + "\n" + action_message
    send_message(DISCORD_PUBLIC_WEBHOOK_URL, full_message)

def send_gap_alert(symbol, gap_info):
    message = (
        f"📢 **התראת גאפ צפוי – פתיחה {gap_info['direction']}**\n"
        f"🧨 מניה: **{symbol}**\n"
        f"📊 גודל הגאפ: {gap_info['gap_pct']}%\n"
        f"🔥 עוצמה: {gap_info['strength']}\n"
        f"⚠️ **הוראת פעולה:** התאם את הפקודה – צפה לתנודתיות גבוהה!"
    )
    send_message(DISCORD_PUBLIC_WEBHOOK_URL, message)
