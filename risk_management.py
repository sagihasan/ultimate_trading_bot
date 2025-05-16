# risk_management.py

from config import DEFAULT_STOP_LOSS_PERCENT, DEFAULT_TAKE_PROFIT_PERCENT

def calculate_stop_loss(entry_price):
    stop_loss = entry_price * (1 - DEFAULT_STOP_LOSS_PERCENT / 100)
    return round(stop_loss, 2)

def calculate_take_profit(entry_price):
    take_profit = entry_price * (1 + DEFAULT_TAKE_PROFIT_PERCENT / 100)
    return round(take_profit, 2)
