# src/keep_alive.py

from flask import Flask, request
from threading import Thread
from datetime import datetime
import pytz
from pytz import timezone

app = Flask(__name__)


@app.route('/')
def home():
    return "הבוט פעיל"


@app.route('/uptime-check', methods=['GET'])
def uptime_check():
    user_agent = request.headers.get('User-Agent', '')

    if 'UptimeRobot' in user_agent:
        print(
            f"[UptimeRobot] Ping at: {datetime.now(pytz.timezone('Asia/Jerusalem')).strftime('%Y-%m-%d %H:%M:%S')}"
        )
        return "UptimeRobot OK", 200
    else:
        print(f"[Unknown Ping] User-Agent: {user_agent}")
        return "Ping received", 200


def run():
    print("⚡ keep_alive server is up and listening on port 8080")
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()
