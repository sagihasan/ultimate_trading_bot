import yfinance as yf

def detect_expected_gap(symbol):
    """
    זיהוי גאפ צפוי בפרי־מרקט (לפני תחילת המסחר)
    """
    try:
        data = yf.Ticker(symbol)
        hist = data.history(period="2d")

        if len(hist) < 2:
            return None

        prev_close = hist["Close"].iloc[-2]
        premarket_open = hist["Open"].iloc[-1]

        gap_pct = ((premarket_open - prev_close) / prev_close) * 100

        if abs(gap_pct) >= 2:  # סף רגישות לגאפ צפוי
            direction = "למעלה (שוק לונג)" if gap_pct > 0 else "למטה (שוק שורט)"
            strength = "חזק" if abs(gap_pct) >= 4 else "בינוני"
            return {
                "gap_pct": round(gap_pct, 2),
                "direction": direction,
                "strength": strength
            }

    except Exception as e:
        print(f"שגיאה בזיהוי גאפ במניה {symbol}: {e}")
    return None
