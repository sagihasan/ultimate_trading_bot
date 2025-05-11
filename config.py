import os
import requests
import time

# מניות למעקב
STOCK_LIST = [
    'PLTR', 'AMZN', 'NVDA', 'AAPL', 'TSLA', 'ANET', 'SNEX', 'CRGY',
    'MSFT', 'GOOG', 'AMD', 'ADBE', 'META', 'AI', 'AR', 'ALSN', 'ASGN',
    'HIMS', 'ASTS', 'HOOD', 'DKNG', 'SOUN', 'APP', 'PZZA', 'AVGO', 'SMCI',
    'ADI', 'SEDG', 'ARKK', 'PERI', 'NU', 'ACHC', 'SMMT', 'ZIM', 'GRPN',
    'RKT', 'EBAY', 'CVNA', 'XBI', 'PANW', 'NFLX', 'ABNB', 'BIDU', 'COIN',
    'CRWD', 'DDOG', 'DOCU', 'ETSY', 'FSLY', 'GDRX', 'GME', 'IQ', 'JD',
    'LI', 'MELI', 'MGNI', 'MOMO', 'MRNA', 'NET', 'NIO', 'OKTA', 'PDD',
    'PINS', 'PTON', 'QCOM', 'ROKU', 'SHOP', 'SNAP', 'SQ', 'TAL', 'TDOC',
    'TME', 'TWLO', 'U', 'UBER', 'VIPS', 'WBA', 'WISH', 'WKHS', 'ZM',
    'BABA', 'CSIQ', 'DKS', 'EA', 'ENPH', 'F', 'GM', 'GS', 'INTC', 'JNJ',
    'KO', 'LMT', 'LOW', 'LULU', 'MCD', 'MRK', 'MS', 'NFLX', 'NVAX',
    'ORCL', 'PEP', 'PYPL', 'SBUX', 'SJM', 'T', 'TSN', 'UNH', 'V', 'VZ',
    'WMT', 'XOM', 'BB', 'CLSK', 'RIOT', 'MARA', 'BTBT', 'HUT', 'BITF',
    'CANO', 'SOFI', 'RIVN', 'LCID', 'AFRM', 'UPST', 'BMBL', 'MTCH', 'CRSP'
]

# ניהול סיכונים מתוך .env
ACCOUNT_SIZE = float(os.getenv("ACCOUNT_SIZE", 951))
RISK_PERCENTAGE = float(os.getenv("RISK_PERCENTAGE", 0.02))
STOP_LOSS_PERCENT = float(os.getenv("STOP_LOSS_PERCENT", 0.03))
TAKE_PROFIT_PERCENT = float(os.getenv("TAKE_PROFIT_PERCENT", 0.05))

# Webhooks
DISCORD_PUBLIC_WEBHOOK = os.getenv("DISCORD_PUBLIC_WEBHOOK")
DISCORD_PRIVATE_WEBHOOK = os.getenv("DISCORD_PRIVATE_WEBHOOK")
DISCORD_ERROR_WEBHOOK = os.getenv("DISCORD_ERROR_WEBHOOK")

# API Keys
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# פונקציית הגנה לשגיאות 429
def safe_get(url, headers=None, params=None, retries=3, delay=15):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                return response
            elif response.status_code == 429:
                print(f"שגיאת 429 – ממתין {delay} שניות (ניסיון {attempt + 1})")
                time.sleep(delay)
            else:
                print(f"שגיאה בקבלת נתונים: {response.status_code}")
                break
        except Exception as e:
            print(f"שגיאה בבקשה: {e}")
            time.sleep(delay)
    return None
