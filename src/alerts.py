# alerts.py
from datetime import datetime, timedelta

macro_events_schedule = [
    {
        "event": "נאום יו\"ר הפד",
        "time": "18:00",
        "strength": "חזק"
    },
    {
        "event": "נתוני CPI",
        "time": "15:30",
        "strength": "חזק"
    },
    {
        "event": "נתוני אבטלה",
        "time": "15:30",
        "strength": "בינוני"
    },
    {
        "event": "מדד מנהלי רכש",
        "time": "17:00",
        "strength": "בינוני"
    },
    {
        "event": "תמ\"ג רבעוני",
        "time": "15:30",
        "strength": "חזק"
    },
]


def parse_time_string(time_str):
    return datetime.strptime(time_str, "%H:%M").time()


def check_macro_events(events):
    now = datetime.now().time()
    one_hour_from_now = (datetime.combine(datetime.today(), now) +
                         timedelta(hours=1)).time()

    upcoming_events = []

    for event in macro_events_schedule:
        event_time = parse_time_string(event["time"])
        if now <= event_time <= one_hour_from_now:
            upcoming_events.append(event)

    return upcoming_events
