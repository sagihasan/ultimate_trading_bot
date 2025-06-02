# scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from macro_analyzer import analyze_macro_calendar
from report_generator import create_pdf_report
from log_my_changes import log_update


def start_scheduler():
    scheduler = BackgroundScheduler()

    # בדיקה כל שעה לאירועים כלכליים
    scheduler.add_job(analyze_macro_calendar, 'interval', hours=1)

    # יצירת דוחות כל יום ראשון בשעה 12:00
    from report_generator import create_pdf_report

    scheduler.add_job(create_pdf_report, 'cron', day_of_week='sun', hour=12)

    # לוג אוטומטי כל יום
    scheduler.add_job(lambda: log_update(
        title="בדיקת מצב מערכת",
        description="בוצעה בדיקה יומית כללית על ידי המתזמן."),
                      'cron',
                      hour=23)

    scheduler.start()
