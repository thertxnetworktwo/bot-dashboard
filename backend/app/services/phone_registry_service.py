import httpx
from typing import List, Optional
from app.core.config import settings
from app.schemas.phone import (
    PhoneCheckRequest,
    PhoneCheckResponse,
    PhoneRegisterRequest,
    PhoneRegisterResponse,
    PhoneBulkRegisterRequest,
    PhoneBulkRegisterResponse,
    PhoneCleanupResponse
)


class PhoneRegistryService:
    """Service for interacting with external phone registry API."""
    
    def __init__(self):
        self.base_url = settings.PHONE_REGISTRY_URL
        self.api_key = settings.PHONE_REGISTRY_API_KEY
        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
    
    async def check_phone(self, phone_number: str) -> PhoneCheckResponse:
        """Check if a phone number exists in the registry."""
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/phone/check",
                    json={"phone_number": phone_number},
                    headers=self.headers
                )
                response.raise_for_status()
                data = response.json()
                return PhoneCheckResponse(**data)
            except httpx.HTTPError as e:
                # Return default response on error
                return PhoneCheckResponse(exists=False, phone_number=phone_number)
    
    async def register_phone(
        self,
        phone_number: str,
        metadata: Optional[dict] = None
    ) -> PhoneRegisterResponse:
        """Register a single phone number."""
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/phone/register",
                    json={"phone_number": phone_number, "metadata": metadata},
                    headers=self.headers
                )
                response.raise_for_status()
                data = response.json()
                return PhoneRegisterResponse(**data)
            except httpx.HTTPError as e:
                return PhoneRegisterResponse(
                    success=False,
                    phone_number=phone_number,
                    message=f"Failed to register: {str(e)}"
                )
    
    async def bulk_register_phones(
        self,
        phone_numbers: List[str],
        metadata: Optional[dict] = None
    ) -> PhoneBulkRegisterResponse:
        """Bulk register up to 1000 phone numbers."""
        if len(phone_numbers) > 1000:
            return PhoneBulkRegisterResponse(
                success=False,
                registered_count=0,
                failed_count=len(phone_numbers),
                failed_numbers=phone_numbers
            )
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/phone/bulk-register",
                    json={"phone_numbers": phone_numbers, "metadata": metadata},
                    headers=self.headers
                )
                response.raise_for_status()
                data = response.json()
                return PhoneBulkRegisterResponse(**data)
            except httpx.HTTPError as e:
                return PhoneBulkRegisterResponse(
                    success=False,
                    registered_count=0,
                    failed_count=len(phone_numbers),
                    failed_numbers=phone_numbers
                )
    
    async def cleanup_old_records(self) -> PhoneCleanupResponse:
        """Cleanup old phone records."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.delete(
                    f"{self.base_url}/api/phone/cleanup",
                    headers=self.headers
                )
                response.raise_for_status()
                data = response.json()
                return PhoneCleanupResponse(**data)
            except httpx.HTTPError as e:
                return PhoneCleanupResponse(
                    success=False,
                    deleted_count=0,
                    message=f"Cleanup failed: {str(e)}"
                )
