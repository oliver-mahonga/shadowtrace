# backend/app/api/ws.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
from .. import schemas, crud
from ..db import AsyncSessionLocal 
import uuid
import os
import redis.asyncio as aioredis 

# Redis client (for action queue)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)

# --- Connection Manager (Singleton for real-time communication) ---
class ConnectionManager:
    """Manages active WebSocket connections for mobile devices."""
    def __init__(self):
        # Dictionary to hold active connections: {unique_device_id: WebSocket}
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, unique_device_id: str):
        await websocket.accept()
        self.active_connections[unique_device_id] = websocket
        print(f"Device connected: {unique_device_id}")

    def disconnect(self, unique_device_id: str):
        self.active_connections.pop(unique_device_id, None)
        print(f"Device disconnected: {unique_device_id}")
        
    async def process_command_queue(self, unique_device_id: str):
        """Pulls commands from the Redis queue upon connection and sends them via WebSocket."""
        queue_key = f"device:{unique_device_id}:actions"
        while (command_json := await redis_client.lpop(queue_key)):
            websocket = self.active_connections.get(unique_device_id)
            if websocket:
                await websocket.send_text(command_json)
                print(f"Command retrieved from queue and SENT to {unique_device_id}")
            else:
                 await redis_client.rpush(queue_key, command_json) 
                 break 

    async def send_command_to_device(self, unique_device_id: str, command_json: str):
        """Sends a command JSON message to a specific device if connected, else queues it."""
        websocket = self.active_connections.get(unique_device_id)
        if websocket:
            await websocket.send_text(command_json)
            print(f"Command SENT directly to {unique_device_id}")
            return True
        else:
            queue_key = f"device:{unique_device_id}:actions"
            await redis_client.rpush(queue_key, command_json)
            print(f"Command QUEUED for {unique_device_id}")
            return False

manager = ConnectionManager()
ws_router = APIRouter(tags=["4. Real-time WebSockets"])

@ws_router.websocket("/ws/device/{unique_device_id}")
async def websocket_endpoint(websocket: WebSocket, unique_device_id: str):
    try:
        await manager.connect(websocket, unique_device_id)
        await manager.process_command_queue(unique_device_id)
        
        while True:
            data = await websocket.receive_text()
            print(f"Received status update from {unique_device_id}: {data}")
            
            try:
                status_payload = schemas.CommandStatusUpdate.model_validate(json.loads(data))
                
                # Update the command log in the database
                async with AsyncSessionLocal() as session:
                    await crud.update_command_log_status(
                        session, 
                        status_payload.command_id, 
                        status_payload.status, 
                        status_payload.payload
                    )
                    print(f"Command ID {status_payload.command_id} updated to {status_payload.status}")

            except Exception as e:
                print(f"Error processing device update: {e}")
                
    except WebSocketDisconnect:
        manager.disconnect(unique_device_id)
    except Exception as e:
        print(f"Critical WebSocket error for {unique_device_id}: {e}")
        manager.disconnect(unique_device_id)