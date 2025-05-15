from fastapi import FastAPI, WebSocket, WebSocketDisconnect , HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import List
from models import Room
from crud import create_room, get_rooms, get_room_by_id, update_room, delete_room
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request


app = FastAPI(
    title="Digital Twin Room Booking",
    description="API pour gérer la réservation de salles",
    version="1.0.0",
)

# Configure les chemins
current_dir = Path(__file__).parent

# Chemin vers le dossier templates
templates = Jinja2Templates(directory=str(current_dir / "templates"))

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    rooms = await get_rooms()
    return templates.TemplateResponse("index.html", {"request": request, "rooms": rooms})



# Liste des connexions WebSocket actives
active_connections: List[WebSocket] = []

# Endpoint WebSocket
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


# Modèle de notification
class RoomNotification(BaseModel):
    id: str
    capacity: int
    occupancy: int
    reserved: bool

# Endpoint pour notifier un changement de salle
@app.post("/notify-room-change")
async def notify_room_change(notification: RoomNotification):
    print(f"Notification reçue : {notification}")
    return JSONResponse(content={"message": "Notification reçue et traitée."}, status_code=200)


# POST: Ajouter une nouvelle salle
@app.post("/rooms/", response_model=Room)
async def api_create_room(room: Room):
    await create_room(room)
    return room

# GET: Obtenir une salle par son ID
@app.get("/rooms/{room_id}", response_model=Room)
async def api_get_room_by_id(room_id: str):
    room = await get_room_by_id(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Salle non trouvée")
    return room

# PUT: Modifier une salle
@app.put("/rooms/{room_id}")
async def api_update_room(room_id: str, room_data: dict):
    await update_room(room_id, room_data)
    return {"message": "Salle mise à jour avec succès"}



async def notify_all(message: str):
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except Exception:
            pass  # ignore les erreurs de connexion


# DELETE: Supprimer une salle
@app.delete("/rooms/{room_id}")
async def api_delete_room(room_id: str):
    room = await get_room_by_id(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Salle non trouvée")
    
    await delete_room(room_id)
    await notify_all(f"Salle supprimée: ID={room.id}, Type={room.type}, Capacité={room.capacity}")
    
    return {"message": "Salle supprimée avec succès"}
