# src/position_utils.py

# סימולציה – בעתיד אפשר לחבר לממשק אמיתי
open_positions_dict = {
    # דוגמה: "AAPL": "לונג"
}

def check_open_position(symbol):
    return symbol in open_positions_dict

def get_position_direction(symbol):
    return open_positions_dict.get(symbol, None)
