try:
    from fastapi import APIRouter, Response
except Exception:  # pragma: no cover - allows editor/static analysis when fastapi isn't installed
    # Minimal fallbacks so linters or environments without fastapi won't error.
    class Response:
        def __init__(self, content=None, media_type=None):
            self.content = content
            self.media_type = media_type

    class APIRouter:
        def __init__(self):
            pass
        def get(self, *args, **kwargs):
            def _decor(f):
                return f
            return _decor
from prometheus_client import Gauge, generate_latest

router = APIRouter()

last_sync = Gauge('last_sync_timestamp', 'Last successful sync')
sync_errors = Gauge('sync_errors_total', 'Total sync errors')

@router.get("/metrics")
async def metrics():
    """Prometheus metrics"""
    data = generate_latest()
    # generate_latest() returns bytes
    return Response(content=data, media_type="text/plain; version=0.0.4; charset=utf-8")