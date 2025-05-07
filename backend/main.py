from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uuid
from models import Room
from crud import create_room, get_all_rooms, get_room_by_id, update_room, delete_room
from typing import List
from pydantic import BaseModel





app = FastAPI(
    title="Digital Twin Room Booking",
    description="API pour gérer la réservation de salles",
    version="1.0.0",
)

frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")



@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join("../frontend", "index.html"))

# Liste des WebSockets connectés pour envoyer les notifications
active_connections: List[WebSocket] = []

# Route WebSocket pour recevoir les notifications en temps réel
@app.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message reçu: {data}")
    except WebSocketDisconnect:
        active_connections.remove(websocket)

# Route pour ajouter une salle et envoyer une notification
@app.post("/rooms/")
async def create(room: Room):
    # Créer la salle dans la base de données
    created_room = await create_room(room)

    # Envoyer une notification à tous les clients connectés
    message = f"Nouvelle salle créée: {created_room.id}"
    for connection in active_connections:
        await connection.send_text(message)

    return created_room

# Lire toutes les salles
@app.get("/rooms/")
async def read_all():
    try:
        rooms = await get_all_rooms()  # Appel à la fonction qui récupère les salles depuis MongoDB
        return {"rooms": rooms}  # Renvoie les salles dans la réponse
    except Exception as e:
        return {"message": "Erreur lors de la récupération des salles", "error": str(e)}
    
# Lire une salle par son ID
@app.get("/rooms/{room_id}")
async def read_one(room_id: str):
    return await get_room_by_id(room_id)

# Mettre à jour une salle
@app.put("/rooms/{room_id}")
async def update(room_id: str, room: Room):
    updated_room = await update_room(room_id, room.dict())
    
    # Envoyer une notification après la mise à jour
    message = f"Salle mise à jour: {updated_room.id}"
    for connection in active_connections:
        await connection.send_text(message)

    return updated_room

# Supprimer une salle
@app.delete("/rooms/{room_id}")
async def delete(room_id: str):
    deleted_room = await delete_room(room_id)
    
    # Envoyer une notification après la suppression
    message = f"Salle supprimée: {deleted_room.id}"
    for connection in active_connections:
        await connection.send_text(message)

    return deleted_room

# Page d'accueil simple pour afficher un message
@app.get("/", response_class=HTMLResponse)
async def get():
    html_content = """
    <html>
        <head>
            <title>Notifications de Salle</title>
        </head>
        <body>
            <h1>Notifications en Temps Réel</h1>
            <div id="notifications"></div>
            <script>
                const notificationsDiv = document.getElementById("notifications");
                const socket = new WebSocket("ws://localhost:8000/ws/notifications");

                socket.onmessage = function(event) {
                    const newNotification = document.createElement("div");
                    newNotification.textContent = event.data;
                    notificationsDiv.appendChild(newNotification);
                };
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

class RoomNotification(BaseModel):
    id: str
    capacity: int
    occupancy: int
    reserved: bool

@app.post("/notify-room-change")
async def notify_room_change(notification: RoomNotification):
    # Ici, tu traites la notification de modification d'une salle
    print(f"Notification reçue : {notification}")
    
    # Tu pourrais aussi, par exemple, mettre à jour la base de données MongoDB en conséquence
    # update_room_in_mongo(notification.id, notification.dict())
    
    return JSONResponse(content={"message": "Notification reçue et traitée."}, status_code=200)