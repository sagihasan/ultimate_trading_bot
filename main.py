# main.py

import os
import time
from datetime import datetime
import pytz
from dotenv import load_dotenv
from discord_manager import create_signal_message

# טוען ENV
load_dotenv()

# קונפיג
from config import (
    STOP_LOSS_PERCENTAGE,
    TAKE_PROFIT_PERCENTAGE,
    RISK_REWARD_RATIO,
    MIN_VOLUME,
    MIN_AI_SCORE,
    MIN_CONFIDENCE_SCORE,
    ACCOUNT_SIZE,
    TIMEZONE,
    MARKET_OPEN_HOUR,
    MARKET_CLOSE_HOUR,
    EARLY_CLOSE_HOUR,
    DST_MARKET_OPEN_HOUR,
    DST_MARKET_CLOSE_HOUR,
    DST_FINAL_SIGNAL_HOUR,
    REGULAR_FINAL_SIGNAL_HOUR,
    EARLY_FINAL_SIGNAL_HOUR
)

# טוען את רשימת המניות מבחוץ
from stock_list import STOCK_LIST

# מודולים פנימיים
from discord_manager import send_discord_message, send_error_message
from fundamentals import analyze_fundamentals, check_upcoming_earnings
from technicals import analyze_technicals
from macro_analyzer import analyze_macro
from log_manager import log_trade
from log_chances import log_chance
from log_my_changes import log_update


def rate_score(score):
    score = int(score)
    if score >= 90:
        return "חזק מאוד"
    elif score >= 75:
        return "חזק"
    elif score >= 60:
        return "בינוני"
    else:
        return "חלש"

def create_trade_signal(ticker):
    try:
        fundamentals = analyze_fundamentals(ticker)
        if not fundamentals:
            return None

        technicals = analyze_technicals(ticker)
        if not technicals:
            return None

        earnings_date, days_until_earnings = check_upcoming_earnings(ticker)
        macro_summary = analyze_macro()

        ai_score = technicals.get("ai_score", 0)
        confidence_score = technicals.get("confidence_score", 0)

        if ai_score < MIN_AI_SCORE or confidence_score < MIN_CONFIDENCE_SCORE:
            return None

        entry_price = technicals["entry_price"]
        stop_loss = round(entry_price * (1 - STOP_LOSS_PERCENTAGE), 2)
        take_profit = round(entry_price * (1 + TAKE_PROFIT_PERCENTAGE), 2)

        risk_dollars = round(ACCOUNT_SIZE * STOP_LOSS_PERCENTAGE, 2)
        reward_dollars = round(ACCOUNT_SIZE * TAKE_PROFIT_PERCENTAGE, 2)

        signal = {
            "ticker": ticker,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "direction": technicals["direction"],
            "order_type": technicals.get("order_type", "Market"),
            "ai_score": f"{ai_score}% ({rate_score(ai_score)})",
            "confidence": f"{confidence_score}% ({rate_score(confidence_score)})",
            "risk_percent": STOP_LOSS_PERCENTAGE * 100,
            "reward_percent": TAKE_PROFIT_PERCENTAGE * 100,
            "risk_dollars": risk_dollars,
            "reward_dollars": reward_dollars,
            "trend": technicals["trend"],
            "zones": technicals["zones"],
            "indicators": technicals["indicators"],
            "fundamental_trend": fundamentals["trend"],
            "sector": fundamentals["sector"],
            "macro_summary": macro_summary,
            "earnings_in": days_until_earnings,
            "has_earnings_tomorrow": days_until_earnings == 1,
        }

        return signal

    except Exception as e:
        send_error_message(f"שגיאה ביצירת איתות ל־{ticker}: {e}")
        return None


def build_signal_message(signal):
    earnings_note = ""
    if signal["has_earnings_tomorrow"]:
        earnings_note = "\n**שים לב:** מחר יש דוח לחברה. צפי להשפעה גבוהה על השוק!"

    order_type = signal.get("order_type", "Market")
    entry_price_line = ""
    if order_type.lower() != "market":
        entry_price_line = f"\nמחיר כניסה מתוכנן: {signal['entry_price']}"

    msg = f"""**איתות לכניסה לעסקה – {signal['ticker']}**
סוג פקודה: {order_type}{entry_price_line}
סטופ לוס: {signal['stop_loss']}
טייק פרופיט: {signal['take_profit']}

תחזית עתידית של החברה:
החברה במצב: {signal['fundamental_trend']} | סקטור: {signal['sector']}

מגמת מניה: {signal['trend']}
אזור טכני: {', '.join(signal['zones'])}
תנועת מחיר: {signal['indicators']}

{earnings_note}

AI Score: {signal['ai_score']}
Confidence Score: {signal['confidence']}

רמת סיכון: {signal['risk_percent']}% | רווח צפוי: {signal['reward_percent']}%
סיכון בדולרים: ${signal['risk_dollars']} | סיכוי בדולרים: ${signal['reward_dollars']}

**הבוט קובע: להיכנס לעסקה מיידית – סיכון נמוך, פוטנציאל גבוה.**
"""
    return msg


def run_bot_on_all_stocks(stock_list):
    best_signal = None

    for ticker in stock_list:
        print(f"בודק את {ticker}...")
        signal = create_trade_signal(ticker)

        if signal:
            if not best_signal or float(signal['ai_score'].split('%')[0]) > float(best_signal['ai_score'].split('%')[0]):
                best_signal = signal

    if best_signal:
        message = build_signal_message(best_signal)
        send_discord_message(message)
        log_trade(best_signal)
        log_chance(
            symbol=best_signal['ticker'],
            risk_percent=best_signal['risk_percent'],
            reward_percent=best_signal['reward_percent'],
            risk_dollars=best_signal['risk_dollars'],
            reward_dollars=best_signal['reward_dollars'],
            ai_score=best_signal['ai_score'],
            confidence_score=best_signal['confidence']
        )
    else:
        send_discord_message("הבוט לא שולח איתות – השוק מסובך או לא תומך.")


def is_dst():
    now = datetime.now(pytz.timezone(TIMEZONE))
    return bool(now.dst())

def is_half_day():
    # כאן אפשר להוסיף זיהוי לפי לוח חגים/ימים מקוצרים
    return False  # עדכון ידני או שילוב עם holidays API


if __name__ == "__main__":
    current_time = datetime.now(pytz.timezone(TIMEZONE))
    now_hour = current_time.hour
    now_minute = current_time.minute

    final_hour = (
        EARLY_FINAL_SIGNAL_HOUR if is_half_day()
        else DST_FINAL_SIGNAL_HOUR if is_dst()
        else REGULAR_FINAL_SIGNAL_HOUR
    )

    if now_hour == final_hour and now_minute >= 40:
        run_bot_on_all_stocks(STOCK_LIST)
