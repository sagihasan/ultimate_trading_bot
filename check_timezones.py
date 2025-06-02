from datetime import datetime
from pytz import timezone


def check_timezone(source_name):
    israel_tz = timezone("Asia/Jerusalem")
    now = datetime.now(israel_tz)
    print(
        f"[{source_name}] השעה בישראל היא: {now.strftime('%Y-%m-%d %H:%M:%S')}"
    )


if __name__ == "__main__":
    # תוכל לקרוא לכל פונקציה או קובץ שאתה רוצה לבדוק
    check_timezone("after_market")
    check_timezone("pre_market")
    check_timezone("main")
    check_timezone("reporting")
    check_timezone("log_manager")
    check_timezone("scheduler")
    check_timezone("keep_alive")
    check_timezone("monthly_planner")
