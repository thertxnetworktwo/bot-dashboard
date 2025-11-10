import httpx
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class PhoneRegistryService:
    """Service to interact with external phone registry API."""

    def __init__(self):
        self.base_url = settings.PHONE_REGISTRY_URL
        self.api_key = settings.PHONE_REGISTRY_API_KEY

    async def check_phone(self, phone_number: str) -> dict:
        """Check if a phone number exists in the registry."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/phone/check",
                    json={"phone_number": phone_number},
                    headers={"X-API-Key": self.api_key},
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error checking phone number: {e}")
            raise Exception(f"Failed to check phone number: {str(e)}")

    async def register_phone(self, phone_number: str) -> dict:
        """Register a phone number in the registry."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/phone/register",
                    json={"phone_number": phone_number},
                    headers={"X-API-Key": self.api_key},
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error registering phone number: {e}")
            raise Exception(f"Failed to register phone number: {str(e)}")

    async def bulk_register_phones(self, phone_numbers: list) -> dict:
        """Bulk register phone numbers."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/phone/bulk-register",
                    json={"phone_numbers": phone_numbers},
                    headers={"X-API-Key": self.api_key},
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error bulk registering phone numbers: {e}")
            raise Exception(f"Failed to bulk register phone numbers: {str(e)}")

    async def cleanup_old_records(self, days: int = 90) -> dict:
        """Cleanup old phone registry records."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self.base_url}/api/phone/cleanup",
                    params={"days": days},
                    headers={"X-API-Key": self.api_key},
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error cleaning up old records: {e}")
            raise Exception(f"Failed to cleanup old records: {str(e)}")
