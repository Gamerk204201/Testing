from sqlalchemy.orm import Session
from .models import SyncAudit

def log_sync_event(db: Session, vehicle_id: str, action: str, details: str = ""):
    event = SyncAudit(
        vehicle_id=vehicle_id,
        action=action,
        details=details
    )
    db.add(event)
    db.commit()