# backend/app/main.py

from fastapi import FastAPI
from .api import v1
from .api import ws 
from .db import engine, Base
import logging
from contextlib import asynccontextmanager

logger = logging.getLogger("uvicorn.error")

# --- Lifespan/Startup Events ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure DB tables are created (development convenience)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("DB tables ensured")
    
    yield # Application runs
    
    logger.info("Application shut down.")


app = FastAPI(
    title="ShadowTrace API", 
    lifespan=lifespan 
)

# --- Include Routers ---
app.include_router(v1.router, prefix="/api") 
app.include_router(ws.ws_router) 

@app.get("/")
async def root():
    return {"message": "ShadowTrace API v1 is running! Access /docs for API schema."}