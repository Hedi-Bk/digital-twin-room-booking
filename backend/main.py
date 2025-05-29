### main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from models import Room, RoomNotification
from crud import create_room, get_all_rooms
from fiware.orion_client import send_room_to_orion
from fiware.subscription import create_room_subscription


import time
import requests

ORION_URL = "http://orion:1026"


app = FastAPI()
templates = Jinja2Templates(directory="templates")

def wait_for_orion():
    url = "http://orion:1026/version"
    for i in range(20):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                print("✅ Orion is ready.")
                return
        except Exception:
            print(f"⌛ Waiting for Orion... ({i+1}/10)")
        time.sleep(3)
    raise Exception("❌ Orion not ready after waiting.")

wait_for_orion()

@app.on_event("startup")
async def startup():
    create_room_subscription()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/rooms/{room_id}", response_model=Room)
async def api_get_room(room_id: str):
    room = get_room_by_id(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Salle non trouvée")
    return room

@app.get("/rooms/")
async def read_rooms():
    return await get_all_rooms()


@app.post("/rooms/")
async def create_new_room(room: Room):
    await create_room(room)
    send_room_to_orion(room)
    return {"message": "Room added and sent to Orion."}



@app.post("/notify-room-change")
async def notify_room_change(notification: RoomNotification):
    print(f"Received notification: {notification}")
    return JSONResponse(content={"message": "Notification processed."})



@app.put("/rooms/{room_id}", response_model=Room)
async def api_update_room(room_id: str, room: Room):
    if room_id != room.id:
        raise HTTPException(status_code=400, detail="L'ID du chemin et du corps ne correspondent pas")
    updated = update_room(room_id, room)
    if not updated:
        raise HTTPException(status_code=404, detail="Salle non trouvée")
    return updated

@app.delete("/rooms/{room_id}", status_code=204)
async def api_delete_room(room_id: str):
    deleted = delete_room(room_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Salle non trouvée")
    return