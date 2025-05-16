# zones.py

def classify_zones(technicals, fundamentals):
    zones = []

    if technicals.get("in_demand_zone"):
        zones.append("Demand Zone")

    if fundamentals.get("in_buffett_zone"):
        zones.append("Buffett Zone")

    # בעתיד – נוכל לזהות גם Golden Zone לפי פיבונאצ'י

    return zones
