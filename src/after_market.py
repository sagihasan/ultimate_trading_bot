import yfinance as yf
from datetime import datetime

def check_after_market_alert():
    now = datetime.now()
    if now.hour < 23:
        return None

    try:
        sp500 = yf.download("^GSPC", period="2d", interval="30m")
        nasdaq = yf.download("^IXIC", period="2d", interval="30m")

        if sp500.empty or nasdaq.empty:
            return "לא ניתן לנתח אפטר מרקט – נתונים חסרים."

        last_sp = sp500["Close"].iloc[-1]
        prev_sp = sp500["Close"].iloc[-2]
        last_nd = nasdaq["Close"].iloc[-1]
        prev_nd = nasdaq["Close"].iloc[-2]

        sp_change = ((last_sp - prev_sp) / prev_sp) * 100
        nd_change = ((last_nd - prev_nd) / prev_nd) * 100

        message = "**עדכון אפטר מרקט:**\n"
        message += f"שינוי ב-S&P 500: {sp_change:.2f}%\n"
        message += f"שינוי בנאסד\"ק: {nd_change:.2f}%\n"

        if sp_change < -0.5 or nd_change < -0.5:
            message += "הערה: ירידות קלות או חזקות באפטר מרקט\n"
        elif sp_change > 0.5 or nd_change > 0.5:
            message += "הערה: עליות קלות או חזקות באפטר מרקט\n"
        else:
            message += "האפטר מרקט שקט יחסית.\n"

        return message

    except Exception as e:
        return f"שגיאה בניתוח אפטר מרקט: {e}"
