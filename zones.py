# zones.py

def is_in_buffett_zone(current_price, intrinsic_value):
    """
    בדיקה אם המחיר הנוכחי נמצא באזור Buffett – כלומר תמחור הוגן עם פוטנציאל לעלייה.
    """
    return 0.9 * intrinsic_value <= current_price <= 1.1 * intrinsic_value

def is_in_golden_zone(fibonacci_retracement):
    """
    בדיקה אם המניה נמצאת באזור Golden Zone לפי רמות פיבונאצ'י.
    Golden Zone מוגדר כ־61.8%–65% תיקון.
    """
    return 0.618 <= fibonacci_retracement <= 0.65

def is_in_demand_zone(current_price, demand_zone_range):
    """
    בדיקה אם המחיר הנוכחי נמצא בתוך אזור ביקוש.
    demand_zone_range הוא tuple (min_price, max_price)
    """
    min_price, max_price = demand_zone_range
    return min_price <= current_price <= max_price

def is_in_bull_flag_pattern(patterns):
    """
    בדיקה אם זוהה תבנית bull flag.
    לדוגמה: אם בתוך patterns יש 'bull_flag' הבדיקה תחזיר True.
    """
    return "bull_flag" in patterns

def is_in_reversal_zone(reversal_patterns):
    """
    בדיקה אם זוהתה פסגה או תחתית היפוך או נר היפוך.
    """
    return any(p in reversal_patterns for p in ["reversal_top", "reversal_bottom", "hammer", "shooting_star"])

def is_in_triangle_pattern(patterns):
    """
    בדיקה אם זוהתה תבנית משולש (symmetrical / ascending / descending).
    """
    return any(p in patterns for p in ["sym_triangle", "asc_triangle", "desc_triangle"])

def is_in_accumulation_phase(volume_profile):
    """
    בדיקה אם מדובר בשלב איסוף לפי פרופיל נפח.
    """
    return volume_profile == "accumulation"

def is_in_distribution_phase(volume_profile):
    """
    בדיקה אם מדובר בשלב הפצה לפי פרופיל נפח.
    """
    return volume_profile == "distribution"

def is_in_expansion_phase(price_behavior):
    """
    בדיקה אם מדובר בשלב תנועה חזקה של מחיר.
    """
    return price_behavior == "expansion"

def is_bullish_market(trend):
    """
    בדיקה האם השוק הכללי שורי לפי מגמה.
    """
    return trend.lower() == "bullish"

def is_bearish_market(trend):
    """
    בדיקה האם השוק הכללי דובי לפי מגמה.
    """
    return trend.lower() == "bearish"
