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

def detects_weakness(symbol):
    data = get_recent_candles(symbol)
    red_candles = [c for c in data[-3:] if c['close'] < c['open'] and c['volume'] > average_volume(symbol)]

    rsi = calculate_rsi(data)
    macd = calculate_macd(data)

    if len(red_candles) >= 2 or (rsi < 40 and macd['hist'] < 0):
        return True
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
