### models.py
from pydantic import BaseModel

class Room(BaseModel):
    id: str
    name: str
    capacity: int
    occupancy: int = 0      # valeur par défaut 0
    reserved: bool = False  # valeur par défaut False

class RoomNotification(BaseModel):
    data: list
