import os
from dotenv import load_dotenv

# טוען את הקובץ .env מהתיקייה הראשית
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

# משתני דיסקורד
DISCORD_PUBLIC_WEBHOOK_URL = os.getenv("DISCORD_PUBLIC_WEBHOOK_URL")
DISCORD_PRIVATE_WEBHOOK_URL = os.getenv("DISCORD_PRIVATE_WEBHOOK_URL")
DISCORD_ERRORS_WEBHOOK_URL = os.getenv("DISCORD_ERRORS_WEBHOOK_URL")
