from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import List
from models import Room
from crud import create_room
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Digital Twin Room Booking",
    description="API pour gérer la réservation de salles",
    version="1.0.0",
)

# Configure les chemins
current_dir = Path(__file__).parent
frontend_dir = current_dir.parent / "Frontend"

# Monte les fichiers statiques
app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

# Sert le frontend
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    return FileResponse(frontend_dir / "index.html")

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
