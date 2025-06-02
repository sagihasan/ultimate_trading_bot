import yfinance as yf
from datetime import datetime
from src.discord_manager import send_error_message
from discord_manager import send_public_message
from pytz import timezone


def check_after_market_alert():
    israel_tz = timezone("Asia/Jerusalem")
    now = datetime.now(israel_tz)
    if now.hour < 23:
        return None

    try:
        sp500 = yf.download("^GSPC", period="2d", interval="30m")
        nasdaq = yf.download("^IXIC", period="2d", interval="30m")

        if sp500.empty or nasdaq.empty:
            return "לא ניתן להוריד נתוני אפטר מרקט"

        last_sp = sp500["Close"].iloc[-1]
        prev_sp = sp500["Close"].iloc[-2]
        last_nd = nasdaq["Close"].iloc[-1]
        prev_nd = nasdaq["Close"].iloc[-2]

        sp_change = ((last_sp - prev_sp) / prev_sp) * 100
        nd_change = ((last_nd - prev_nd) / prev_nd) * 100

        message = "**זיהוי אפטר מרקט**\n"
        message += f"שינוי ב־S&P 500: {sp_change:.2f}%\n"
        message += f"שינוי בנאסד״ק: {nd_change:.2f}%\n"

        if sp_change < -0.5 or nd_change < -0.5:
            message += "\nהערכה: ירידות קלות או חזקות באפטר מרקט"
        elif sp_change > 0.5 or nd_change > 0.5:
            message += "\nהערכה: עליות קלות או חזקות באפטר מרקט"
        else:
            message += "\nהאפטר מרקט שקט יחסית"

        send_message_with_delay(send_public_message, message)

    except Exception as e:
        send_error_message(f"שגיאה באפטר מרקט: {e}")
