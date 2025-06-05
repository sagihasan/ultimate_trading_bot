# risk_management.py

from config import DEFAULT_STOP_LOSS_PERCENT, DEFAULT_TAKE_PROFIT_PERCENT
from config import PORTFOLIO_SIZE

def calculate_position_size(entry_price, stop_loss_price, risk_percent=2):
    risk_amount = (risk_percent / 100) * PORTFOLIO_SIZE
    position_size = risk_amount / abs(entry_price - stop_loss_price)
    return max(1, int(position_size))

def calculate_stop_loss(entry_price, direction='long'):
    stop_loss = entry_price * (1 - DEFAULT_STOP_LOSS_PERCENT / 100) if direction == 'long' else entry_price * (1 + DEFAULT_STOP_LOSS_PERCENT / 100)
    return round(stop_loss, 2)

def calculate_take_profit(entry_price, direction='long'):
    take_profit = entry_price * (1 + DEFAULT_TAKE_PROFIT_PERCENT / 100) if direction == 'long' else entry_price * (1 - DEFAULT_TAKE_PROFIT_PERCENT / 100)
    return round(take_profit, 2)

def detect_premarket_weakness(symbol):
    return detects_weakness(symbol, direction="לונג") or detects_weakness(symbol, direction="שורט")

def detect_live_weakness(symbol):
    return detects_weakness(symbol, direction="לונג") or detects_weakness(symbol, direction="שורט")

def detect_aftermarket_weakness(symbol):
    return detects_weakness(symbol, direction="לונג") or detects_weakness(symbol, direction="שורט")

def detect_crisis(symbol):
    # סימולציה – תחליף בעתיד באינדיקטורים חכמים יותר
    vix = get_vix_level()
    market_trend = get_sp500_trend()
    volume = get_current_volume(symbol)
    rsi = get_current_rsi(symbol)

    crisis_indicators = []

    if vix > 25:
        crisis_indicators.append("VIX גבוה – תנודתיות קיצונית")
    if market_trend == "ירידה חדה":
        crisis_indicators.append("ירידה חדה ב־S&P 500")
    if rsi < 30:
        crisis_indicators.append("RSI נמוך מאוד – לחץ מכירה חזק")
    if volume > 2 * average_volume(symbol):
        crisis_indicators.append("נפח מסחר גבוה פי 2 מהממוצע")

    if len(crisis_indicators) >= 2:
        direction = "למטה"
        summary = "\n".join(f"• {line}" for line in crisis_indicators)
        return True, direction, summary

    # תוכל להוסיף גם זיהוי משבר לונג (אופוריה)
    if rsi > 80 and market_trend == "עלייה חדה" and vix < 14:
        summary = (
            "• RSI גבוה מאוד\n"
            "• מגמת עלייה חדה בשוק\n"
            "• VIX נמוך – שקט מדומה לפני סערה"
        )
        return True, "למעלה", summary

    return False, None, None

def detect_bubble_conditions(sp500_trend, nasdaq_trend, vix_level, pe_ratio, volume_surge, direction):
    bubble_signs = 0

    if direction == "לונג":
        if sp500_trend == "עלייה חדה":
            bubble_signs += 1
        if nasdaq_trend == "עלייה חדה":
            bubble_signs += 1
        if vix_level < 14:
            bubble_signs += 1
        if pe_ratio > 25:
            bubble_signs += 1
        if volume_surge:
            bubble_signs += 1

    elif direction == "שורט":
        if sp500_trend == "ירידה חדה":
            bubble_signs += 1
        if nasdaq_trend == "ירידה חדה":
            bubble_signs += 1
        if vix_level > 25:
            bubble_signs += 1
        if pe_ratio < 12:
            bubble_signs += 1
        if volume_surge:
            bubble_signs += 1

    return bubble_signs >= 3

def is_position_open(symbol):
    # לדוגמה – בדיקה אם הסימול נמצא ברשימת הפוזיציות:
    return symbol in current_positions  # current_positions = רשימת המניות עם עסקאות פתוחות

# שמירת רשימת פוזיציות פתוחות
current_positions = []

def is_position_open(symbol):
    return symbol in current_positions

def open_position(symbol):
    if symbol not in current_positions:
        current_positions.append(symbol)

def close_position(symbol):
    if symbol in current_positions:
        current_positions.remove(symbol)

def detects_weakness(symbol, direction):
    data = get_recent_candles(symbol)
    recent = data[-5:]
    rsi = calculate_rsi(data)
    macd = calculate_macd(data)
    avg_vol = average_volume(symbol)
    ma20 = get_moving_average(data, 20)
    current_price = recent[-1]['close']
    fib = calculate_fibonacci_level(data)
    bollinger = calculate_bollinger_bands(data)

    red_candles = [c for c in recent if c['close'] < c['open'] and c['volume'] > avg_vol]
    green_candles = [c for c in recent if c['close'] > c['open'] and c['volume'] > avg_vol]

    if direction == "לונג":
        return (
            len(red_candles) >= 2 or
            current_price < ma20 or
            rsi < 40 or
            macd['hist'] < 0 or
            current_price < fib['61.8'] or
            current_price < bollinger['lower'] or
            is_bearish_engulfing(recent) or
            detect_triangle_pattern(data) or
            detect_flag_pattern(data) or
            detects_reversal_peak(data)
        )
    
    elif direction == "שורט":
        return (
            len(green_candles) >= 2 or
            current_price > ma20 or
            rsi > 60 or
            macd['hist'] > 0 or
            current_price > fib['61.8'] or
            current_price > bollinger['upper'] or
            is_bullish_engulfing(recent) or
            detect_triangle_pattern(data) or
            detect_flag_pattern(data) or
            detects_reversal_valley(data)
        )
    
    return False

def evaluate_risk_reward(entry_price, stop_loss, take_profit):
    risk = abs(entry_price - stop_loss)
    reward = abs(take_profit - entry_price)
    ratio = reward / risk if risk != 0 else 0
    risk_percent = (risk / entry_price) * 100
    reward_percent = (reward / entry_price) * 100

    risk_level = "נמוכה" if risk_percent <= 2 else "גבוהה"
    opportunity_level = "גבוהה" if reward_percent >= 4 else "נמוכה"

    return {
        "risk_percent": round(risk_percent, 2),
        "reward_percent": round(reward_percent, 2),
        "risk_level": risk_level,
        "opportunity_level": opportunity_level,
        "risk_reward_ratio": round(ratio, 2)
    }
