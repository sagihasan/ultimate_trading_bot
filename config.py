import os
from dotenv import load_dotenv

load_dotenv()

# הגדרות כלליות לחשבון וסיכון
ACCOUNT_SIZE = float(os.getenv("ACCOUNT_SIZE", 951))
RISK_PERCENTAGE = float(os.getenv("RISK_PERCENTAGE", 2))
STOP_LOSS_PERCENT = float(os.getenv("STOP_LOSS_PERCENT", 3))
TAKE_PROFIT_PERCENT = float(os.getenv("TAKE_PROFIT_PERCENT", 6))

# Webhooks
DISCORD_PUBLIC_WEBHOOK_URL = os.getenv("DISCORD_PUBLIC_WEBHOOK_URL")
DISCORD_PRIVATE_WEBHOOK_URL = os.getenv("DISCORD_PRIVATE_WEBHOOK_URL")
DISCORD_ERROR_WEBHOOK_URL = os.getenv("DISCORD_ERROR_WEBHOOK_URL")

# API Keys
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

