

# 🏢 Digital Twin - Réservation de Salles

## 📌 Contexte

Ce projet propose une solution de **Digital Twin** pour la gestion de réservation de salles. Chaque salle est modélisée numériquement et son état (réservée, libre, occupation, etc.) est mis à jour via une API simulée.
Le système est construit autour de composants FIWARE et Docker pour assurer l’interopérabilité, la visualisation en temps réel, et l’archivage des données.

---

## 🧠 Objectifs

* Simuler l’état de salles (occupation, disponibilité).
* Mettre à jour les entités NGSI dans le **Contexte Broker Orion**.
* Configurer **Draco** pour persister les données vers **MySQL**.
* Visualiser les informations via une interface web simple.
* Fournir une solution basée sur **Docker Compose**.

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

## 🚀 Lancer l'application

1. Lancer Docker : `docker compose up -d`
2. Simuler des mises à jour avec un script Python ou Node.js.
3. Accéder à l'interface web locale pour voir les salles.

---

## 📊 Résultats

Voici une capture d’écran de l’interface web avec la visualisation des salles (à ajouter plus tard) :

![Capture](./screenshots/dashboard.png)

---

Souhaites-tu que je t’aide à rédiger le script simulateur (en Python ou JS) pour qu’il envoie les données à Orion ?
