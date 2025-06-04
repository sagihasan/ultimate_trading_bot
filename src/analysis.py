from fundamentals import get_fundamental_summary
from technicals import get_technical_summary
from sentiment import get_market_sentiment

# סימולציה של רשימת מניות
stock_list = [
    "AAPL", "MSFT", "NVDA", "GOOG", "AMZN", "META", "TSLA", "AMD", "ADBE",
    "AVGO", "NFLX", "INTC", "CRM", "ORCL", "QCOM", "CSCO", "SHOP", "SNOW",
    "PLTR", "UBER", "BABA", "TCEHY", "LRCX", "ASML", "MU", "TXN", "PANW",
    "SMCI", "SEDG", "ENPH", "ZM", "DOCU", "SQ", "PYPL", "COIN", "SOFI", "ROKU",
    "DDOG", "NET", "ZS", "CROX", "DKNG", "HOOD", "HIMS", "PERI", "APP", "AI",
    "SOUN", "ANET", "SNEX", "ABT", "PZZA", "ALSN", "AR", "TEAM", "FSLR", "RUN",
    "BLNK", "LCID", "RIVN", "NIO", "XPEV", "LI", "CHPT", "TTD", "TWLO", "ATVI",
    "EA", "INTU", "ABNB", "LYFT", "WBD", "WMT", "COST", "TGT", "LOW", "HD",
    "SBUX", "MCD", "PEP", "KO", "JNJ", "MRK", "PFE", "CVX", "XOM", "APA",
    "FANG", "OXY", "SLB", "HAL", "WFC", "BAC", "C", "JPM", "GS", "MS", "BX",
    "SCHW", "V", "MA", "AXP", "TROW", "BK", "AMP", "SPY", "QQQ", "DIA", "IWM",
    "XLK", "XLF", "XLE", "XLY", "XLV", "XLP"
]


def analyze_all_stocks():
    signals = []

    for symbol in stock_list:
        try:
            # ניתוח פונדומנטלי
            fundamental_result = get_fundamental_summary(symbol)

            # ניתוח טכני
            technical_result = get_technical_summary(symbol)

            # ניתוח סנטימנט
            sentiment_result = get_market_sentiment(symbol)

            # תנאים בסיסיים לדוגמה (ניתן לשנות לפי הלוגיקה שלך)
            if (fundamental_result["score"] >= 3
                    and technical_result["score"] >= 3
                    and sentiment_result["sentiment"] == "Positive"):
                signal = {
                    "symbol": symbol,
                    "fundamental": fundamental_result,
                    "technical": technical_result,
                    "sentiment": sentiment_result,
                }
                signals.append(signal)

        except Exception as e:
            print(f"שגיאה בניתוח המניה {symbol}: {e}")

    return signals
