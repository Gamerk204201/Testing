import logging
from tenacity import retry, stop_after_attempt, wait_exponential
from gallagher import cc
from gallagher.cc.cardholders import Cardholder
from minestar_gallagher.configuration import settings

logger = logging.getLogger(__name__)
cc.api_key = settings.gallagher_api_key

# Gallagher will be called via localhost (no IP)
cc.base_url = settings.gallagher_base_url   # ← Uses localhost:8904

COMPETENCY_NAME = "AOZ_MINESTAR_AUTHORISED"

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=30))
async def update_vehicle_authorisation(vehicle_cardholder_id: str, is_authorised: bool, reason: str = "MineStar update"):
    try:
        ch = await Cardholder.get(id=vehicle_cardholder_id)
        
        if is_authorised:
            await ch.add_competency(name=COMPETENCY_NAME)
            logger.info("competency.enabled", vehicle=vehicle_cardholder_id, reason=reason)
        else:
            await ch.remove_competency(COMPETENCY_NAME)
            logger.info("competency.disabled", vehicle=vehicle_cardholder_id, reason=reason)
        
        return True
    except Exception as e:
        logger.error("gallagher.update_failed", vehicle=vehicle_cardholder_id, error=str(e))
        raise