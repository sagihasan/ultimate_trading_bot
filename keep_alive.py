# keep_alive.py

from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "הבוט פעיל!"

def run_server():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    thread = threading.Thread(target=run_server)
    thread.start()
