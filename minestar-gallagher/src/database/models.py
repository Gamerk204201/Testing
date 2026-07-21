from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from datetime import datetime
from .session import Base

class SyncAudit(Base):
    __tablename__ = "sync_audit"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    vehicle_id = Column(String(50))
    operator_id = Column(String(50))
    action = Column(String(30))          # authorised, revoked
    details = Column(Text)
    success = Column(Boolean, default=True)