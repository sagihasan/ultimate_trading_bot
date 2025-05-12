# run_all.py (קובץ ריצה משולב)

import threading
import time
from main import main as run_main
from scheduler import run_scheduler

if __name__ == "__main__":
    # שרשור ראשון – הפעלת הבוט היומי לאיתותים
    main_thread = threading.Thread(target=run_main)
    main_thread.start()

    # שרשור שני – הפעלת ניהול עסקאות ודוחות
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    # שמירה על ריצה רציפה
    while True:
        time.sleep(60)
