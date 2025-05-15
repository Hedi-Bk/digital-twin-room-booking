from database import rooms_collection
from models import Room

async def create_room(room: Room):
    await rooms_collection.insert_one(room.dict())

async def get_rooms():
    rooms = []
    async for room in rooms_collection.find():
        rooms.append(Room(**room))
    return rooms

async def get_room_by_id(room_id: str):
    room = await rooms_collection.find_one({"id": room_id})
    if room:
        return Room(**room)
    return None

async def update_room(room_id: str, room_data: dict):
    await rooms_collection.update_one({"id": room_id}, {"$set": room_data})

async def delete_room(room_id: str):
    await rooms_collection.delete_one({"id": room_id})
