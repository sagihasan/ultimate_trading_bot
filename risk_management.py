from config import DEFAULT_STOP_LOSS_PERCENT, DEFAULT_TAKE_PROFIT_PERCENT

def calculate_stop_loss(entry_price, direction):
    if direction == "long":
        return round(entry_price * (1 - DEFAULT_STOP_LOSS_PERCENT / 100), 2)
    elif direction == "short":
        return round(entry_price * (1 + DEFAULT_STOP_LOSS_PERCENT / 100), 2)

def calculate_take_profit(entry_price, direction):
    if direction == "long":
        return round(entry_price * (1 + DEFAULT_TAKE_PROFIT_PERCENT / 100), 2)
    elif direction == "short":
        return round(entry_price * (1 - DEFAULT_TAKE_PROFIT_PERCENT / 100), 2)
