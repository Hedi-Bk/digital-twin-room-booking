from models import Room
from database import rooms_collection

async def create_room(room: Room):
    return await rooms_collection.insert_one(room.dict())

async def get_all_rooms():
    rooms = await rooms_collection.find().to_list(100)
    return rooms

async def get_room_by_id(room_id: str):
    return await rooms_collection.find_one({"id": room_id})

async def update_room(room_id: str, data: dict):
    return await rooms_collection.update_one({"id": room_id}, {"$set": data})

async def delete_room(room_id: str):
    return await rooms_collection.delete_one({"id": room_id})

import requests

def send_to_orion(room: Room):
    payload = {
        "id": room.id,
        "type": "Room",
        "capacity": {"value": room.capacity, "type": "Integer"},
        "occupancy": {"value": room.occupancy, "type": "Integer"},
        "reserved": {"value": room.reserved, "type": "Boolean"},
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post("http://localhost:1026/v2/entities", json=payload, headers=headers)
    return response.status_code

async def get_all_rooms_from_orion():
    response = requests.get("http://localhost:1026/v2/entities?type=Room")
    if response.status_code == 200:
        rooms = response.json()
        return rooms
    else:
        return {"error": "Failed to fetch rooms from Orion"}
    
def create_subscription():
    subscription_payload = {
        "description": "Subscription for Room changes",
        "subject": {
            "entities": [
                {"id": "Room", "type": "Room"}
            ],
            "condition": {
                "attrs": ["capacity", "occupancy", "reserved"]
            }
        },
        "notification": {
            "http": {
                "url": "http://localhost:8000/notify-room-change"  # Ton endpoint pour recevoir les notifications
            }
        },
        "throttling": 5  # Fréquence des notifications, 5 secondes ici
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post("http://localhost:1026/v2/subscriptions", json=subscription_payload, headers=headers)
    if response.status_code == 201:
        print("Subscription created successfully.")
    else:
        print("Failed to create subscription.")