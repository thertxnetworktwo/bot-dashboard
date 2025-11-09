from pydantic import BaseModel, Field
from typing import Optional, List


class PhoneCheckRequest(BaseModel):
    phone_number: str = Field(..., description="Phone number to check")


class PhoneCheckResponse(BaseModel):
    exists: bool
    phone_number: str


class PhoneRegisterRequest(BaseModel):
    phone_number: str = Field(..., description="Phone number to register")
    metadata: Optional[dict] = None


class PhoneRegisterResponse(BaseModel):
    success: bool
    phone_number: str
    message: Optional[str] = None


class PhoneBulkRegisterRequest(BaseModel):
    phone_numbers: List[str] = Field(..., max_length=1000, description="List of phone numbers (max 1000)")
    metadata: Optional[dict] = None


class PhoneBulkRegisterResponse(BaseModel):
    success: bool
    registered_count: int
    failed_count: int
    failed_numbers: Optional[List[str]] = None


class PhoneCleanupResponse(BaseModel):
    success: bool
    deleted_count: int
    message: Optional[str] = None
