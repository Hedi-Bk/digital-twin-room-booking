### fiware/orion_client.py
import requests
import json

ORION_URL = "http://orion:1026/v2/entities"

def send_room_to_orion(room):
    payload = {
        "id": room.id,
        "type": "Room",
        "name": {"type": "Text", "value": room.name},
        "capacity": {"type": "Integer", "value": room.capacity}
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(ORION_URL, data=json.dumps(payload), headers=headers)
    print("Orion response:", response.status_code, response.text)

