import os

# גודל תיק וניהול סיכונים
ACCOUNT_SIZE = float(os.getenv("ACCOUNT_SIZE", 1000))
RISK_PERCENTAGE = float(os.getenv("RISK_PERCENTAGE", 0.02))
STOP_LOSS_PERCENT = float(os.getenv("STOP_LOSS_PERCENTAGE", 0.03))
TAKE_PROFIT_PERCENT = float(os.getenv("TAKE_PROFIT_PERCENTAGE", 0.06))

# Webhooks
DISCORD_PUBLIC_WEBHOOK = os.getenv("DISCORD_PUBLIC_WEBHOOK")
DISCORD_ERROR_WEBHOOK = os.getenv("DISCORD_ERROR_WEBHOOK")
DISCORD_PRIVATE_WEBHOOK = os.getenv("DISCORD_PRIVATE_WEBHOOK")

# API Keys
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# רשימת מניות נטענת בקובץ נפרד בשם stock_list.py

