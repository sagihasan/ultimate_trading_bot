import os
from dotenv import load_dotenv
from dotenv import load_dotenv
import os

def load_env():
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path)

# Load the .env file from the root directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)

DISCORD_PUBLIC_WEBHOOK_URL = os.getenv("DISCORD_PUBLIC_WEBHOOK_URL")
DISCORD_PRIVATE_WEBHOOK_URL = os.getenv("DISCORD_PRIVATE_WEBHOOK_URL")
DISCORD_ERRORS_WEBHOOK_URL = os.getenv("DISCORD_ERRORS_WEBHOOK_URL")
