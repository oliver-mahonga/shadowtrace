# backend/app/api/ws.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

@router.websocket("/ws/track/{device_id}")
async def live_tracking(ws: WebSocket, device_id: str):
    await ws.accept()
    try:
        while True:
            # client may send 'ping' or subscribe messages; keep connection alive
            msg = await ws.receive_text()
            # echo for now; later you will push real location updates to connected sockets
            await ws.send_text(msg)
    except WebSocketDisconnect:
        return
