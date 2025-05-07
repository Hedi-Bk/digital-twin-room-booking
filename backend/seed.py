from faker import Faker
import asyncio
import uuid
from crud import create_room
from models import Room

# Crée une instance de Faker pour générer des données fictives
fake = Faker()

# Fonction asynchrone pour ajouter des salles dans la base de données
async def seed_data(n=10):
    for _ in range(n):
        # Crée une salle avec des données fictives
        room = Room(
            id=str(uuid.uuid4()),  # Utilisation d'un UUID pour l'id de la salle
            type=fake.random_element(elements=("meeting", "conference", "training")),
            capacity=fake.random_int(min=5, max=50),
            occupancy=fake.random_int(min=0, max=10),
            reserved=fake.boolean()
        )
        # Insère la salle dans la base de données
        await create_room(room)
    print(f"{n} rooms added!")

# Point d'entrée du script
if __name__ == "__main__":
    asyncio.run(seed_data())  # Appelle la fonction asynchrone pour ajouter des salles
