from typing import Optional
from sqlalchemy.orm import Session

from minestar_gallagher.database.models import VehicleMapping, OperatorMapping


def get_gallagher_vehicle_id(db: Session, minestar_call_sign: str) -> Optional[str]:
    row = (
        db.query(VehicleMapping)
        .filter(
            VehicleMapping.minestar_call_sign == minestar_call_sign.strip().upper(),
            VehicleMapping.active == True,  # noqa: E712
        )
        .one_or_none()
    )
    return row.gallagher_cardholder_id if row else None


def upsert_vehicle_mapping(
    db: Session,
    call_sign: str,
    gallagher_cardholder_id: str,
    href: str = None,
    description: str = None,
) -> VehicleMapping:
    call_sign = call_sign.strip().upper()
    row = (
        db.query(VehicleMapping)
        .filter(VehicleMapping.minestar_call_sign == call_sign)
        .one_or_none()
    )
    if row:
        row.gallagher_cardholder_id = gallagher_cardholder_id
        row.gallagher_href = href
        if description:
            row.description = description
        row.active = True
    else:
        row = VehicleMapping(
            minestar_call_sign=call_sign,
            gallagher_cardholder_id=gallagher_cardholder_id,
            gallagher_href=href,
            description=description,
        )
        db.add(row)
    db.commit()
    return row