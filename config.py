import os
from dotenv import load_dotenv

load_dotenv()

# הגדרות חשבון וניהול סיכון
ACCOUNT_SIZE = float(os.getenv("ACCOUNT_SIZE", 951))  # גודל תיק מעודכן
RISK_PERCENTAGE = float(os.getenv("RISK_PERCENTAGE", 2))
STOP_LOSS_PERCENT = float(os.getenv("STOP_LOSS_PERCENT", 3))
TAKE_PROFIT_PERCENT = float(os.getenv("TAKE_PROFIT_PERCENT", 6))

# Webhooks לשליחה לדיסקורד
DISCORD_PUBLIC_WEBHOOK = os.getenv("DISCORD_PUBLIC_WEBHOOK")
DISCORD_PRIVATE_WEBHOOK = os.getenv("DISCORD_PRIVATE_WEBHOOK")
DISCORD_ERROR_WEBHOOK = os.getenv("DISCORD_ERROR_WEBHOOK")

# API Keys
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# רשימת מניות ייחודיות (126 מניות)
STOCK_LIST = sorted(list(set([
    "AAPL", "MSFT", "NVDA", "GOOG", "AMZN", "META", "TSLA", "AMD", "ADBE", "AVGO",
    "NFLX", "INTC", "CRM", "ORCL", "QCOM", "CSCO", "SHOP", "SNOW", "PLTR", "UBER",
    "BABA", "TCEHY", "LRCX", "ASML", "MU", "TXN", "PANW", "SMCI", "SEDG", "ENPH",
    "ZM", "DOCU", "SQ", "PYPL", "COIN", "SOFI", "ROKU", "DDOG", "NET", "ZS",
    "CROX", "DKNG", "HOOD", "HIMS", "PERI", "APP", "AI", "SOUN", "ANET", "SNEX",
    "CRGY", "ARKK", "NU", "ACHC", "SMMT", "ZIM", "GRPN", "RKT", "EBAY", "CVNA",
    "XBI", "PZZA", "ALSN", "AR", "ASGN", "ASTS", "ADI", "TEAM", "FSLR", "RUN",
    "BLNK", "LCID", "RIVN", "NIO", "XPEV", "LI", "CHPT", "TTD", "TTWO", "ATVI",
    "EA", "INTUIT", "ABNB", "LYFT", "WBD", "WMT", "COST", "TGT", "LOW", "HD",
    "SBUX", "MCD", "PEP", "KO", "JNJ", "MRK", "PFE", "CVX", "XOM", "APA",
    "FANG", "OXY", "SLB", "HAL", "WFC", "BAC", "C", "JPM", "GS", "MS",
    "BX", "SCHW", "V", "MA", "AXP", "TROW", "BK", "AMP", "SPY", "QQQ",
    "DIA", "IWM", "XLK", "XLF", "XLE", "XLY", "XLV", "XLP"
])))

