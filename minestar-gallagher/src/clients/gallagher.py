"""
Gallagher client – controls AOZ_MINESTAR_AUTHORISED competency
on vehicle cardholders.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from minestar_gallagher.configuration import settings

logger = logging.getLogger(__name__)

COMPETENCY_NAME = "AOZ_MINESTAR_AUTHORISED"


class GallagherError(Exception):
    """Permanent Gallagher failure."""


class GallagherClient:
    def __init__(self):
        self.base_url = settings.gallagher_base_url.rstrip("/")
        self.api_key = settings.gallagher_api_key

        # Default to False for internal servers (change later if you have proper CA)
        verify_ssl = getattr(settings, "gallagher_verify_ssl", False)

        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"GGL-API-KEY {self.api_key}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            verify=verify_ssl,
            timeout=30.0,
        )
        self._competency_href: Optional[str] = None

    async def close(self):
        await self.client.aclose()


    async def _get(self, path: str) -> dict:
        resp = await self.client.get(path)
        resp.raise_for_status()
        return resp.json()

    async def _patch(self, path: str, payload: dict) -> dict:
        resp = await self.client.patch(path, json=payload)
        resp.raise_for_status()
        return resp.json() if resp.content else {}

    async def _get_competency_href(self) -> str:
        if self._competency_href:
            return self._competency_href

        data = await self._get("/api/competencies")
        for item in data.get("results", []):
            if item.get("name") == COMPETENCY_NAME:
                self._competency_href = item["href"]
                return self._competency_href

        raise GallagherError(f"Competency '{COMPETENCY_NAME}' not found")

    async def get_cardholder(self, cardholder_id: str) -> dict:
        return await self._get(f"/api/cardholders/{cardholder_id}")

    async def find_competency_link(
        self, cardholder: dict, competency_href: str
    ) -> Optional[str]:
        """Return the link href if the competency is already present."""
        competencies = cardholder.get("competencies", {})
        results = competencies.get("results") or competencies.get("items") or []

        for link in results:
            comp = link.get("competency") or {}
            if comp.get("href") == competency_href:
                return link.get("href")
            # Fallback for older response shapes
            if link.get("href") and competency_href.split("/")[-1] in link.get("href", ""):
                return link.get("href")
        return None

    @retry(
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=1, min=2, max=20),
        retry=retry_if_exception_type((httpx.TransportError, httpx.TimeoutException)),
        reraise=True,
    )
    async def set_vehicle_authorisation(
        self,
        gallagher_cardholder_id: str,
        authorised: bool,
        *,
        expiry_minutes: int = 15,
        reason: str = "MineStar update",
    ) -> bool:

        competency_href = await self._get_competency_href()
        cardholder = await self.get_cardholder(gallagher_cardholder_id)
        existing_link = await self.find_competency_link(cardholder, competency_href)

        if authorised:
            expiry = datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes)

            if existing_link:
                # Renew / re-enable
                payload = {
                    "competencies": {
                        "update": [
                            {
                                "href": existing_link,
                                "enabled": True,
                                "expiry": expiry.isoformat(),
                            }
                        ]
                    }
                }
                action = "renewed"
            else:
                # Add new
                payload = {
                    "competencies": {
                        "add": [
                            {
                                "competency": {"href": competency_href},
                                "enabled": True,
                                "expiry": expiry.isoformat(),
                            }
                        ]
                    }
                }
                action = "enabled"
        else:
            if not existing_link:
                logger.info(
                    "competency.already_absent vehicle=%s reason=%s",
                    gallagher_cardholder_id,
                    reason,
                )
                return True

            payload = {
                "competencies": {
                    "remove": [{"href": existing_link}]
                }
            }
            action = "disabled"

        try:
            await self._patch(f"/api/cardholders/{gallagher_cardholder_id}", payload)
            logger.info(
                "competency.%s vehicle=%s reason=%s",
                action,
                gallagher_cardholder_id,
                reason,
            )
            return True
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 409:
                logger.warning(
                    "gallagher.cardholder_locked vehicle=%s", gallagher_cardholder_id
                )
                raise
            logger.error(
                "gallagher.update_failed vehicle=%s status=%s body=%s",
                gallagher_cardholder_id,
                e.response.status_code,
                e.response.text,
            )
            raise GallagherError(str(e)) from e