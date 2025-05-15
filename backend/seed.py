import uuid
from faker import Faker
from models import Room
from crud import create_room
import asyncio

fake = Faker()

async def seed_data(n=10):
    for _ in range(n):
        room = Room(
            id=str(uuid.uuid4()),
            type=fake.random_element(elements=("meeting", "conference", "training")),
            capacity=fake.random_int(min=5, max=50),
            occupancy=fake.random_int(min=0, max=10),
            reserved=fake.boolean()
        )
        await create_room(room)
    print(f"{n} rooms added!")

if __name__ == "__main__":
    asyncio.run(seed_data())
