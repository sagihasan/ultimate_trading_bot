from fundamentals import analyze_fundamentals
from technicals import analyze_technicals
from macro import get_macro_data, get_index_trend, is_market_bullish
from discord_manager import send_discord_message, create_signal_message
from config import *
from stock_list import STOCK_LIST
import yfinance as yf
import datetime


from macro import is_market_bullish

# בתוך הפונקציה שמבצעת ניתוח
macro_summary = get_macro_summary()
market_bullish = is_market_bullish(macro_summary)

# הכנס לדוח הסופי או איתות
signal["macro_summary"] = macro_summary
signal["market_bullish"] = market_bullish


def run_bot():
    today = datetime.datetime.now().date()
    macro_summary = get_macro_data()
    sp500_trend = get_index_trend('^GSPC')
    nasdaq_trend = get_index_trend('^IXIC')
    vix_trend = get_index_trend('^VIX')

    market_summary = {
        "sp500": {"daily": "עלה" if sp500_trend == "שורי" else "ירד"},
        "nasdaq": {"daily": "עלה" if nasdaq_trend == "שורי" else "ירד"},
        "vix_trend": {"daily": "יורד" if vix_trend == "דובי" else "עולה"}
    }

    market_bullish = is_market_bullish(market_summary)

    for ticker in STOCK_LIST:
        try:
            df = yf.download(ticker, period="6mo")
            if df is None or df.empty:
                continue

            technicals = analyze_technicals(df)
            fundamentals = analyze_fundamentals(ticker)

            signal_data = {
                "ticker": ticker,
                "entry_price": technicals.get("entry_price", 0),
                "stop_loss": 0,
                "take_profit": 0,
                "direction": technicals.get("direction", "N/A"),
                "order_type": technicals.get("order_type", "Market"),
                "ai_score": 80,
                "confidence_score": 85,
                "risk_pct": 3,
                "reward_pct": 6,
                "risk_dollars": 300,
                "reward_dollars": 600,
                "trend_sentiment": technicals.get("trend", "neutral"),
                "zones": str(technicals.get("zones", {})),
                "macro_summary": macro_summary,
                "index_trend": {
                    "S&P 500": sp500_trend,
                    "Nasdaq": nasdaq_trend
                },
                "market_bullish": market_bullish
            }

            message = create_signal_message(signal_data)
            send_discord_message(message)

        except Exception as e:
            error_message = f"שגיאה עבור {ticker}: {str(e)}"
            send_discord_message(error_message, is_error=True)
