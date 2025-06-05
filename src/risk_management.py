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
