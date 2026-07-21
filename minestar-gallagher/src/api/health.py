from fastapi import APIRouter  # type: ignore[import]

router = APIRouter(prefix="/api", tags=["health"])

@router.get("/health")
async def health():
    """Basic health check"""
    return {
        "status": "healthy",
        "service": "MineStar-Gallagher Sync"
    }