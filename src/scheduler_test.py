from discord_manager import send_private_message
from datetime import datetime

def simulate_start_and_end():
    now = datetime.now()
    start_message = f"הבוט התחיל לפעול - {now.strftime('%Y-%m-%d %H:%M')}"
    end_message = f"הבוט סיים את הפעולה - {now.strftime('%Y-%m-%d %H:%M')}"

    # שליחת ההודעות לדיסקורד לבדיקה
    send_private_message(start_message)
    send_private_message(end_message)

if __name__ == "__main__":
    simulate_start_and_end()
