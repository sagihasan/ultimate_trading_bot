import os
from datetime import datetime
from config import DISCORD_PRIVATE_WEBHOOK
from utils import send_discord_message

CHANGELOG_FILE = "CHANGELOG.md"
SENT_LOG_FILE = "last_sent_changelog.txt"

def get_latest_changelog_entry():
    if not os.path.exists(CHANGELOG_FILE):
        return None

    with open(CHANGELOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    entry = []
    capture = False
    for line in lines:
        if line.startswith("## ["):
            if capture:
                break
            capture = True
        if capture:
            entry.append(line)

    return "".join(entry).strip()

def already_sent(entry_title):
    if not os.path.exists(SENT_LOG_FILE):
        return False
    with open(SENT_LOG_FILE, "r") as f:
        return f.read().strip() == entry_title

def mark_as_sent(entry_title):
    with open(SENT_LOG_FILE, "w") as f:
        f.write(entry_title)

def send_latest_changelog():
    entry = get_latest_changelog_entry()
    if not entry:
        return

    title_line = entry.splitlines()[0].strip()
    if already_sent(title_line):
        return

    message = f"**עדכון גרסה אחרון לבוט:**\n```markdown\n{entry}\n```"
    send_discord_message(DISCORD_PRIVATE_WEBHOOK, message, message_type="update")
    mark_as_sent(title_line)
