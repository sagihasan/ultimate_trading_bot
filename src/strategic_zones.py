def check_strategic_zones(symbol, data):
    # ניתוח Golden Zone לפי פיבונאצ'י
    high = max(c['high'] for c in data)
    low = min(c['low'] for c in data)
    current_price = data[-1]['close']

    golden_zone_top = low + 0.618 * (high - low)
    golden_zone_bottom = low + 0.5 * (high - low)

    in_golden_zone = golden_zone_bottom <= current_price <= golden_zone_top

    # אזור ביקוש / היצע (פשוט לדוגמה)
    demand_zone = low + 0.1 * (high - low)
    supply_zone = high - 0.1 * (high - low)

    in_demand_zone = current_price <= demand_zone
    in_supply_zone = current_price >= supply_zone

    # Buffett Zone – הערכת שווי פשוטה לדוגמה
    pe = get_company_pe(symbol)
    in_buffett_zone = pe < 15

    zones = []
    if in_golden_zone:
        zones.append("Golden Zone")
    if in_demand_zone:
        zones.append("Demand Zone")
    if in_supply_zone:
        zones.append("Supply Zone")
    if in_buffett_zone:
        zones.append("Buffett Zone")

    return zones
