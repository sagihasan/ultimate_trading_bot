# changelog_manager.py

from datetime import datetime

CHANGELOG_FILE = "CHANGELOG.md"

def log_update(title, description, start_date=None, end_date=None):
    today = datetime.today().strftime("%Y-%m-%d")
    if not start_date:
        start_date = today
    if not end_date:
        end_date = today

    date_range = start_date if start_date == end_date else f"{start_date} עד {end_date}"

    log_entry = f"""### {title}
**תאריך עדכון:** {today}  
**טווח עבודה:** {date_range}  
**מה השתנה:**  
{description}

---
"""

    try:
        with open(CHANGELOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
        print("העדכון נרשם בהצלחה ל־CHANGELOG.md")

    except Exception as e:
        print(f"שגיאה בעדכון CHANGELOG: {e}")
