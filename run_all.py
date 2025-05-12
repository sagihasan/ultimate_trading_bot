import threading
import time
from main import main as run_main
from scheduler import run_scheduler

if __name__ == "__main__":
    main_thread = threading.Thread(target=run_main)
    main_thread.start()

    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    while True:
        time.sleep(60)
