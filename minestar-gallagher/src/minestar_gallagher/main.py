import asyncio
import uvicorn
from fastapi import FastAPI

from minestar_gallagher.logging_config import setup_logging
from minestar_gallagher.database import init_db
from minestar_gallagher.services.synchronisation import daily_full_sync

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="MineStar-Gallagher Sync Service")

# Include API routers
from minestar_gallagher.api.health import router as health_router
from minestar_gallagher.api.status import router as status_router
from minestar_gallagher.api.metrics import router as metrics_router

app.include_router(health_router)
app.include_router(status_router)
app.include_router(metrics_router)

@app.get("/")
async def root():
    return {"message": "MineStar-Gallagher Sync Service is running"}

def start_service():
    init_db()
    logger.info("Service starting...")

    # You can add the scheduler here if you want it in the same process
    # For Windows Service, it's better to keep it in service.py

if __name__ == "__main__":
    start_service()
    uvicorn.run(app, host="127.0.0.1", port=8765)