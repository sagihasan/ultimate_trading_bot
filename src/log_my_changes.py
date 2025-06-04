from datetime import datetime
from pytz import timezone

CHANGELOG_PATH = "CHANGELOG.md"


def log_update(title, description, start_date=None, end_date=None):
    try:
        israel_tz = timezone("Asia/Jerusalem")
        now = datetime.now(israel_tz).strftime("%Y-%m-%d %H:%M")
        start_str = f"מתאריך {start_date}" if start_date else ""
        end_str = f"עד {end_date}" if end_date else ""
        date_range = f"{start_str} {end_str}".strip()

        log_entry = f"""
### {title}
- תיאור: {description}
- {date_range}
- נרשם בתאריך: {now}
---
"""

        with open(CHANGELOG_PATH, "a", encoding="utf-8") as f:
            f.write(log_entry)

        print("העדכון נרשם בקובץ CHANGELOG.md")

    except Exception as e:
        print(f"שגיאה ברישום שינויים: {e}")
