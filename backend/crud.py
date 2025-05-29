### crud.py
from models import Room
import httpx


ORION_URL = "http://orion:1026/v2/entities"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
# 🔹 Create Room
async def create_room(room: Room):
    async with httpx.AsyncClient() as client:
        response = await client.post(ORION_URL, json=room.dict(), headers=HEADERS)
        response.raise_for_status()
        return room

# 🔹 Get all rooms
async def get_all_rooms():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ORION_URL}?type=Room", headers={"Accept": "application/json"})
        response.raise_for_status()
        return response.json()

# 🔹 Get one room
async def get_room_by_id(room_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ORION_URL}/{room_id}", headers={"Accept": "application/json"})
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

# 🔹 Update room (remplacement complet)
async def update_room(room_id: str, updated_data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.patch(f"{ORION_URL}/{room_id}/attrs", json=updated_data, headers=HEADERS)
        response.raise_for_status()
        return updated_data

# 🔹 Delete room
async def delete_room(room_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{ORION_URL}/{room_id}", headers=HEADERS)
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return True