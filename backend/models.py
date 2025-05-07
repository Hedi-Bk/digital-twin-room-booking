from pydantic import BaseModel

class Room(BaseModel):
    id: str
    type: str
    capacity: int
    occupancy: int
    reserved: bool

# 1. Définition du modèle RoomNotification
