# backend/app/main.py

from fastapi import FastAPI
from .api import v1
from .api import ws 
from .db import engine, Base
import logging
from contextlib import asynccontextmanager
from sqlalchemy import text # Required for executing raw SQL

logger = logging.getLogger("uvicorn.error")

# --- Lifespan/Startup Events ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure DB tables are created (development convenience)
    async with engine.begin() as conn:
        
        # 1. ENSURE UUID EXTENSION IS AVAILABLE
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')) 
        
        # 2. ENSURE POSTGIS EXTENSION IS AVAILABLE (NEW FIX)
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS postgis'))
        
        # 3. Create tables
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