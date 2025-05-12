import threading
import time
from main import main as run_main
from scheduler import run_scheduler

if __name__ == "__main__":
    # תהליך ראשון – הבוט היומי (איתותים)
    main_thread = threading.Thread(target=run_main)
    main_thread.start()

    # תהליך שני – ניהול עסקאות ודוחות
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    # שמירה על תהליכים רצים
    while True:
        time.sleep(60)
