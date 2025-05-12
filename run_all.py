from main import main
from scheduler import run_scheduler
import threading

if __name__ == "__main__":
    # הפעלת ניהול עסקאות ודוחות ברקע
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    # הרצת הבוט הראשי של האיתות
    main()

    # ממתין לסיום של scheduler (רק אם תרצה)
    scheduler_thread.join()
