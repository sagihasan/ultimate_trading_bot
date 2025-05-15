from datetime import datetime

def log_change(file, description):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {file}: {description}\n"
    with open("CHANGELOG.md", "a", encoding="utf-8") as f:
        f.write(line)
