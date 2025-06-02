# src/uptime_checker.py

from flask import request


@app.route('/uptime-check', methods=['GET'])
def uptime_check():
    user_agent = request.headers.get('User-Agent', '')
    if 'UptimeRobot' in user_agent:
        print(
            "[UptimeRobot] Ping detected at:",
            datetime.now(
                pytz.timezone('Asia/Jerusalem')).strftime('%Y-%m-%d %H:%M:%S'))
        return "UptimeRobot OK", 200
    else:
        print("[Unknown Ping] From:", user_agent)
        return "Ping received", 200
