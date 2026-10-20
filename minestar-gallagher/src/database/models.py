from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    Boolean,
)

from .session import Base


class VehicleMapping(Base):
    """MineStar Call Sign -> Gallagher vehicle cardholder"""
    __tablename__ = "vehicle_mapping"

    id = Column(Integer, primary_key=True)
    minestar_call_sign = Column(String(50), unique=True, nullable=False, index=True)
    gallagher_cardholder_id = Column(String(50), nullable=False)
    gallagher_href = Column(String(255))
    description = Column(String(255))
    active = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class OperatorMapping(Base):
    """MineStar Operator ID -> Gallagher / TAMS Personnel ID"""
    __tablename__ = "operator_mapping"

    id = Column(Integer, primary_key=True)
    minestar_operator_id = Column(String(50), unique=True, nullable=False, index=True)
    gallagher_personnel_id = Column(String(50), nullable=False)
    notes = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AuthorisationState(Base):
    """Last known desired & applied state for each vehicle"""
    __tablename__ = "authorisation_state"

    id = Column(Integer, primary_key=True)
    vehicle_call_sign = Column(String(50), unique=True, nullable=False, index=True)
    gallagher_cardholder_id = Column(String(50))

    desired_authorised = Column(Boolean, default=False)
    applied_authorised = Column(Boolean, default=False)

    operator_id = Column(String(50))
    last_minestar_ts = Column(DateTime)
    last_applied_at = Column(DateTime)
    last_reason = Column(String(255))

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SyncAudit(Base):
    __tablename__ = "sync_audit"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    vehicle_call_sign = Column(String(50), index=True)
    operator_id = Column(String(50))
    action = Column(String(30))          # enabled / disabled / renewed / skipped
    success = Column(Boolean, default=True)
    details = Column(Text)
    correlation_id = Column(String(50))


class FailedOperation(Base):
    """retry queue"""
    __tablename__ = "failed_operation"

    id = Column(Integer, primary_key=True)
    operation_type = Column(String(50))
    vehicle_call_sign = Column(String(50))
    payload = Column(Text)
    attempt_count = Column(Integer, default=0)
    next_attempt_at = Column(DateTime)
    last_error = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    status = Column(String(20), default="pending")