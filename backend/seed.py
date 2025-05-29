import requests
import random

def random_room_name():
    names = ["Salle de sport", "Salle de reunion", "Salle de conference", "Salle deattente", "Salle de travail"]
    return random.choice(names)

def seed_rooms():
    for i in range(5,10):
        room = {
            "id": f"room{i+1}",
            "type": "Room",
            "name": {
                "type": "Text",
                "value": random_room_name()
            },
            "capacity": {
                "type": "Integer",
                "value": random.randint(5, 20)
            },
            "occupancy": {
                "type": "Integer",
                "value": 0
            },
            "reserved": {
                "type": "Boolean",
                "value": False
            }
        }
        print(f"Envoi de la salle {room['id']} à Orion...")
        response = requests.post('http://orion:1026/v2/entities', json=room)
        print(f"Status code: {response.status_code}")
        if response.status_code == 201:
            print(f"Salle {room['id']} insérée avec succès.")
        else:
            print(f"Erreur lors de l'insertion de la salle {room['id']}: {response.text}")

if __name__ == "__main__":
    seed_rooms()
