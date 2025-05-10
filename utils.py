import requests

def send_discord_message(webhook_url, message):
    data = {"content": message}
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("ההודעה נשלחה בהצלחה ✅")
    else:
        print(f"שגיאה בשליחת ההודעה ❌: {response.status_code}")
