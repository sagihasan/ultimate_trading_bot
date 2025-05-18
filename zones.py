def identify_zones(df):
    result = {
        "in_golden_zone": False,
        "in_demand_zone": False
    }

    # Ensure enough data
    if len(df) < 60:
        return result

    high = df["High"].rolling(window=60).max().iloc[-1]
    low = df["Low"].rolling(window=60).min().iloc[-1]
    current_price = df["Close"].iloc[-1]

    # Calculate Fibonacci retracement levels
    diff = high - low
    golden_zone_top = high - diff * 0.618
    golden_zone_bottom = high - diff * 0.786

    # Check if current price is in the Golden Zone
    if golden_zone_bottom <= current_price <= golden_zone_top:
        result["in_golden_zone"] = True

    # Demand Zone logic: identify a recent low with spike in volume
    recent_lows = df.iloc[-20:]
    low_volume_zone = recent_lows[recent_lows["Low"] == recent_lows["Low"].min()]
    if not low_volume_zone.empty and low_volume_zone["Volume"].iloc[0] > df["Volume"].mean():
        result["in_demand_zone"] = True

    return result
