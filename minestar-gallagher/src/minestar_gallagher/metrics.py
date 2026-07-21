from prometheus_client import Gauge, generate_latest
from fastapi import APIRouter

router = APIRouter()

# Simple metrics
last_successful_sync = Gauge('last_sync_timestamp', 'Last successful sync time')
sync_error_count = Gauge('sync_errors_total', 'Total number of sync errors')

@router.get("/metrics")
async def metrics():
    """Prometheus compatible metrics"""
    return generate_latest()