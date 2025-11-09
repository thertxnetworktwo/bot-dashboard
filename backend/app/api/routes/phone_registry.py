from fastapi import APIRouter, HTTPException
from app.schemas.phone import (
    PhoneCheckRequest,
    PhoneCheckResponse,
    PhoneRegisterRequest,
    PhoneRegisterResponse,
    PhoneBulkRegisterRequest,
    PhoneBulkRegisterResponse,
    PhoneCleanupResponse
)
from app.services.phone_registry_service import PhoneRegistryService

router = APIRouter(prefix="/api/phone", tags=["phone-registry"])


@router.post("/check", response_model=PhoneCheckResponse)
async def check_phone(request: PhoneCheckRequest):
    """Check if a phone number exists in the registry."""
    service = PhoneRegistryService()
    result = await service.check_phone(request.phone_number)
    return result


@router.post("/register", response_model=PhoneRegisterResponse)
async def register_phone(request: PhoneRegisterRequest):
    """Register a single phone number."""
    service = PhoneRegistryService()
    result = await service.register_phone(request.phone_number, request.metadata)
    return result


@router.post("/bulk-register", response_model=PhoneBulkRegisterResponse)
async def bulk_register_phones(request: PhoneBulkRegisterRequest):
    """Bulk register up to 1000 phone numbers."""
    if len(request.phone_numbers) > 1000:
        raise HTTPException(
            status_code=400,
            detail="Maximum 1000 phone numbers allowed per request"
        )
    
    service = PhoneRegistryService()
    result = await service.bulk_register_phones(
        request.phone_numbers,
        request.metadata
    )
    return result


@router.delete("/cleanup", response_model=PhoneCleanupResponse)
async def cleanup_old_records():
    """Cleanup old phone records."""
    service = PhoneRegistryService()
    result = await service.cleanup_old_records()
    return result
