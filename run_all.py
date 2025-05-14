from main import main
from scheduler import run_scheduler
from changelog_manager import send_latest_changelog
import threading
import time

if __name__ == "__main__":
    # שליחת גרסת עדכון אחרונה לערוץ הפרטי (אם טרם נשלחה)
    send_latest_changelog()

    # הפעלת ניהול עסקאות ודוחות ברקע
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    # הרצת הבוט הראשי של האיתותים
    main()

    # המתנה לסיום של הסקדולר (לא חובה – אפשר גם להשאיר פתוח)
    scheduler_thread.join()
