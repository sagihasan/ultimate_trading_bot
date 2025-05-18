# trade_manager.py

from trade_management import create_trade_entry, log_trade_result, load_open_trades, save_open_trades
from datetime import datetime

def evaluate_trade_exit(trade, current_price):
    direction = trade["סוג עסקה"]
    stop_loss = trade["סטופ לוס"]
    take_profit = trade["טייק פרופיט"]
    entry_price = trade["מחיר כניסה"]

    # עבור לונג
    if direction == "לונג":
        if current_price <= stop_loss:
            return "סטופ לוס"
        elif current_price >= take_profit:
            return "טייק פרופיט"
    # עבור שורט
    elif direction == "שורט":
        if current_price >= stop_loss:
            return "סטופ לוס"
        elif current_price <= take_profit:
            return "טייק פרופיט"

    return None

def update_open_trades(current_prices):
    open_trades = load_open_trades()
    updated_trades = []
    for trade in open_trades:
        symbol = trade["מניה"]
        if symbol in current_prices:
            result = evaluate_trade_exit(trade, current_prices[symbol])
            if result:
                trade["תוצאה"] = result
                trade["(%)] תשואה"] = calculate_return(trade, current_prices[symbol])
                log_trade_result(trade)
            else:
                updated_trades.append(trade)
        else:
            updated_trades.append(trade)
    save_open_trades(updated_trades)

def calculate_return(trade, exit_price):
    entry = trade["מחיר כניסה"]
    direction = trade["סוג עסקה"]
    if direction == "לונג":
        return round(((exit_price - entry) / entry) * 100, 2)
    elif direction == "שורט":
        return round(((entry - exit_price) / entry) * 100, 2)
    return 0

def open_new_trade(symbol, direction, entry_price, stop_loss, take_profit, reason, zone, market_rating):
    new_trade = create_trade_entry(
        symbol=symbol,
        direction=direction,
        entry_price=entry_price,
        stop_loss=stop_loss,
        take_profit=take_profit,
        reason=reason,
        zone=zone,
        market_rating=market_rating
    )
    trades = load_open_trades()
    trades.append(new_trade)
    save_open_trades(trades)
