from fastapi import APIRouter  # type: ignore[import]
from datetime import datetime

router = APIRouter()

@router.get("/status")
async def status():
    """Service status with basic info"""
    return {
        "status": "running",
        "uptime": "see Windows Service Manager",
        "last_sync": "check logs or audit table",
        "gallagher": "localhost:8904",
        "minestar": "connected via SQL"
    }