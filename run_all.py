from main import main
from scheduler import run_scheduler
from changelog_manager import send_latest_changelog
import threading
import time

if __name__ == "__main__":
    send_latest_changelog()  # שליחת יומן עדכונים לערוץ הפרטי

    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    time.sleep(2)
    main()

    scheduler_thread.join()
