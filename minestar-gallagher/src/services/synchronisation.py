import asyncio
import logging
from datetime import datetime
from minestar_gallagher.clients.minestar import get_current_qualifications
from minestar_gallagher.clients.gallagher import update_vehicle_authorisation
from minestar_gallagher.database import SessionLocal
from minestar_gallagher.database.models import SyncAudit

logger = logging.getLogger(__name__)

async def daily_full_sync():
    """Main sync - MineStar is source of truth"""
    start = datetime.now()
    logger.info("sync.started")

    db = SessionLocal()
    success_count = 0

    try:
        current_states = await get_current_qualifications()

        for vehicle_id, data in current_states.items():
            try:
                success = await update_vehicle_authorisation(
                    vehicle_cardholder_id=vehicle_id,
                    is_authorised=data.get("is_authorised", False),
                    reason=data.get("reason", "MineStar update")
                )
                if success:
                    success_count += 1
                    audit = SyncAudit(
                        vehicle_id=vehicle_id,
                        action="authorised" if data.get("is_authorised") else "revoked",
                        details=data.get("reason")
                    )
                    db.add(audit)
                    db.commit()
                await asyncio.sleep(0.7)
            except Exception as e:
                logger.error("sync.vehicle_error", vehicle=vehicle_id, error=str(e))
                db.rollback()

        logger.info("sync.completed", success=success_count, total=len(current_states))
    except Exception as e:
        logger.critical("sync.failed", error=str(e))
    finally:
        db.close()