
````markdown
# 🏢 Digital Twin - Gestion intelligente de réservation de salles

## 📝 Contexte

Ce projet propose une solution basée sur le concept de *Digital Twin* pour la gestion de la réservation de salles dans un bâtiment (université, entreprise, etc.). Chaque salle est représentée comme une entité numérique permettant de suivre sa disponibilité en temps réel. Les mises à jour proviennent d’une API simulée, sans capteurs physiques.

Des notifications sont générées si une salle est occupée sans réservation ou si des conflits apparaissent.

## 🧩 Technologies utilisées

- [FIWARE Orion Context Broker](https://fiware-orion.readthedocs.io/) – Gestion du contexte des salles et des réservations
- [Draco (NiFi)](https://fiware-draco.readthedocs.io/) – Transfert des données vers MySQL
- [MySQL] – Stockage des historiques de réservation
- [Docker / Docker Compose] – Conteneurisation de l’architecture
- [Fake REST API] – Injection simulée des réservations/états d’occupation

## 📦 Modèles de données (NGSI v2)

### Exemple : Salle

```json
{
  "id": "urn:ngsi-ld:Room:101",
  "type": "Room",
  "name": "Salle 101",
  "capacity": 30,
  "status": "occupied",
  "currentReservation": "urn:ngsi-ld:Booking:001"
}
````

### Exemple : Réservation

```json
{
  "id": "urn:ngsi-ld:Booking:001",
  "type": "Booking",
  "room": "urn:ngsi-ld:Room:101",
  "startTime": "2025-05-06T09:00:00Z",
  "endTime": "2025-05-06T10:30:00Z",
  "reservedBy": "John Doe"
}
```

## ⚙️ Installation (Docker Compose)

```bash
git clone https://github.com/ton-utilisateur/room-booking-digital-twin.git
cd room-booking-digital-twin
docker compose up -d
```

### Extrait du fichier `docker-compose.yml`

```yaml
version: '3.1'
services:
  orion:
    image: fiware/orion
    ports:
      - "1026:1026"
  mysql:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: example
    ports:
      - "3306:3306"
  draco:
    image: ging/fiware-draco
    ports:
      - "9090:9090"
```

## 🚀 Lancer l'application

1. Lancer les conteneurs avec `docker compose up -d`
2. Injecter les données via les endpoints API simulés (`curl`, Postman ou script Python)
3. Observer les changements sur l’entité Room via l’interface Orion ou la base de données

## ✅ Résultats attendus

* Visualisation de la disponibilité des salles en temps réel
* Détection automatique de conflits de réservation
* Historique de l’occupation enregistré dans MySQL

## 📸 Captures d'écran

*Ajouter ici des captures de l’interface Orion, des données stockées, ou de ton dashboard personnalisé*

---

## 🧑‍💻 Auteur

Ce projet a été réalisé dans le cadre d’un exercice sur les Digital Twins par \[Ton Nom].

---

📌 N’oublie pas d’ajouter un fichier `.env` ou un dossier `scripts/` si tu as des scripts d’injection.

```

Souhaites-tu que je t’aide aussi à créer les premiers fichiers du projet ?
```
