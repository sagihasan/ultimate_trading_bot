import threading
from main import main
from scheduler import run_scheduler
import time

if __name__ == "__main__":
    try:
        # הפעלת ניהול עסקאות ודוחות ברקע
        scheduler_thread = threading.Thread(target=run_scheduler)
        scheduler_thread.start()

        # הרצת הבוט הראשי של האיתותים
        main()

        # המתנה בלולאה כדי שהבוט יישאר פעיל בענן
        while True:
            time.sleep(60)

    except Exception as e:
        print(f"שגיאה בהרצת run_all.py: {e}")
