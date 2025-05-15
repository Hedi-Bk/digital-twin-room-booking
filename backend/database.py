from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://mongo:27017")
db = client["room_reservation"]
rooms_collection = db["rooms"]
