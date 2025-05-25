def identify_zones(df):
    result = {
        "in_golden_zone": False,
        "in_demand_zone": False,
        "in_supply_zone": False,
        "in_buffett_zone": False
    }

    if len(df) < 60:
        return result

    high = df["High"].rolling(window=60).max().iloc[-1]
    low = df["Low"].rolling(window=60).min().iloc[-1]
    current_price = df["Close"].iloc[-1]

    # Golden Zone
    diff = high - low
    golden_top = high - diff * 0.618
    golden_bottom = high - diff * 0.786
    if golden_bottom <= current_price <= golden_top:
        result["in_golden_zone"] = True

    # Demand Zone
    recent_lows = df.iloc[-20:]
    low_vol = recent_lows[recent_lows["Low"] == recent_lows["Low"].min()]
    if not low_vol.empty and low_vol["Volume"].iloc[0] > df["Volume"].mean():
        result["in_demand_zone"] = True

    # Supply Zone
    recent_highs = df.iloc[-20:]
    high_vol = recent_highs[recent_highs["High"] == recent_highs["High"].max()]
    if not high_vol.empty and high_vol["Volume"].iloc[0] > df["Volume"].mean():
        result["in_supply_zone"] = True

    # Buffett Zone – פונדומנטלי בלבד (מנוהל ב־fundamentals.py)
    result["in_buffett_zone"] = False

    return result
