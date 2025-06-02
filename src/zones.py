def detect_strategic_zones(df):
    try:
        high = df["High"].rolling(window=60).max().iloc[-1]
        low = df["Low"].rolling(window=60).min().iloc[-1]
        current_price = df["Close"].iloc[-1]

        golden_zone_top = high - (high - low) * 0.618
        golden_zone_bottom = high - (high - low) * 0.786

        in_golden_zone = golden_zone_bottom <= current_price <= golden_zone_top

        recent_lows = df.iloc[-20:]
        low_volume_zone = recent_lows[recent_lows["Low"] ==
                                      recent_lows["Low"].min()]
        in_demand_zone = False

        if not low_volume_zone.empty and low_volume_zone["Volume"].iloc[
                0] > df["Volume"].mean():
            in_demand_zone = True

        return {
            "in_golden_zone": in_golden_zone,
            "in_demand_zone": in_demand_zone
        }

    except Exception as e:
        print(f"שגיאה בזיהוי אזורים אסטרטגיים: {e}")
        return {"in_golden_zone": False, "in_demand_zone": False}
