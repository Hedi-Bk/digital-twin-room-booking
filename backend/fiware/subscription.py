### fiware/subscription.py
import requests
import json

ORION_URL = "http://orion:1026/v2/subscriptions"

def create_room_subscription():
    payload = {
        "description": "Notify backend on room changes",
        "subject": {
            "entities": [
                {"idPattern": ".*", "type": "Room"}
            ],
            "condition": {"attrs": ["name", "capacity"]}
        },
        "notification": {
            "http": {"url": "http://backend:8000/notify-room-change"},
            "attrs": ["name", "capacity"]
        },
        "throttling": 5
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(ORION_URL, data=json.dumps(payload), headers=headers)
    print("Subscription response:", response.status_code, response.text)
