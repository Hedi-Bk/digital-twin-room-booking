

# 🏢 Digital Twin - Réservation de Salles

Ce projet est une application de démonstration de **jumeau numérique pour la réservation de salles**. Il permet de :

- Gérer des salles avec leurs capacités, taux d’occupation, et état de réservation.
- Visualiser et manipuler ces données via une API REST construite avec **FastAPI**.
- Synchroniser les entités de salle avec un **Orion Context Broker (FIWARE)**.
- Stocker les données dans une base **MongoDB**.
- Offrir une interface web simple pour afficher les informations.

---

## 🛠️ Technologies utilisées

- **FastAPI** : Backend web pour exposer les endpoints REST.
- **MongoDB** : Base de données NoSQL pour stocker les salles.
- **Motor** : Driver asynchrone pour MongoDB avec Python.
- **FIWARE Orion Context Broker** : Pour centraliser les informations contextuelles.
- **Docker & Docker Compose** : Pour orchestrer tous les services.
- **Frontend statique** (HTML/CSS/JS) : Interface légère de visualisation.


---

## 🧱 Architecture du projet

```plaintext
       
       +----------------+
       |   Fake API     |
       |  (simulateur)  |
       +--------+-------+
                |
                |  (NGSI v2 - REST API)
                v
   +-----------------------------+
   |   Orion Context Broker      |
   |          (FIWARE)           |
   +--------------+--------------+
                  |
                  v
       +--------------------+
       |     MongoDB        |
       |  (Base de données) |
       +--------------------+

```

### 🔄 Flux de données

1. **Fake API** simule les événements liés aux salles (réservations, disponibilité...).
2. **Orion Context Broker** reçoit ces données et gère les entités contextuelles.
3. **Draco** écoute les changements sur Orion et les persiste vers **MySQL**.
4. Une **interface web** permet de consulter l’état des salles en temps réel.


Souhaites-tu aussi un schéma illustré sous forme d’image ?





## 📦 Modèles de données

Exemple d'entité JSON (Room) utilisée :

```json
{
  "id": "Room001",
  "type": "Room",
  "status": {
    "type": "Text",
    "value": "reserved"
  },
  "capacity": {
    "type": "Integer",
    "value": 30
  },
  "currentOccupancy": {
    "type": "Integer",
    "value": 20
  }
}
```

---

## ⚙️ Installation (Docker Compose)

### Prérequis

* Docker + Docker Compose
* Git

### Étapes :

```bash
git clone https://github.com/tonuser/digital-twin-room-booking.git
cd digital-twin-room-booking
docker compose up -d
```

---

## 📂 Contenu du `docker-compose.yml`

* `orion` : broker de contexte (mise à jour des données NGSI).
* `mongo` : base de données support pour Orion.
* `draco` : collecte et transformation des données en provenance d'Orion.
* `mysql` : stockage final des données.

---

## 🔁 Fonctionnalités principales

GET /rooms/ : liste toutes les salles enregistrées

POST /rooms/ : ajoute une nouvelle salle

PUT /rooms/{id} : met à jour une salle

DELETE /rooms/{id} : supprime une salle

POST /notify-room-change : endpoint pour recevoir les notifications de changement (NGSI)



## 🚀 Lancer l'application

1. Lancer Docker : `docker compose up -d`
2. Simuler des mises à jour avec un script Python ou Node.js.
3. Accéder à l'interface web locale pour voir les salles.

---

## 📊 Résultats

Voici une capture d’écran de l’interface web des API disponible :

![image](https://github.com/user-attachments/assets/a590bd2a-d08c-427d-97a4-8dd75aa35259)


---

Souhaites-tu que je t’aide à rédiger le script simulateur (en Python ou JS) pour qu’il envoie les données à Orion ?
