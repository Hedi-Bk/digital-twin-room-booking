from pydantic import BaseModel

class Room(BaseModel):
    id: str
    type: str
    capacity: int
    occupancy: int
    reserved: bool
