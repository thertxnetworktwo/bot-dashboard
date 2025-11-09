from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID
import enum


class ProductStatus(str, enum.Enum):
    ACTIVE = "Active"
    EXPIRED = "Expired"
    EXPIRING_SOON = "ExpiringSoon"


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    bot_username: Optional[str] = Field(None, max_length=255)
    website_link: Optional[str] = Field(None, max_length=500)
    contract_months: int = Field(..., ge=1, le=12)
    customer_telegram: Optional[str] = Field(None, max_length=255)
    customer_link: Optional[str] = Field(None, max_length=500)


class ProductCreate(ProductBase):
    contract_start_date: Optional[datetime] = None
    
    @field_validator('contract_start_date')
    @classmethod
    def set_default_start_date(cls, v):
        return v or datetime.utcnow()


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    bot_username: Optional[str] = Field(None, max_length=255)
    website_link: Optional[str] = Field(None, max_length=500)
    contract_months: Optional[int] = Field(None, ge=1, le=12)
    customer_telegram: Optional[str] = Field(None, max_length=255)
    customer_link: Optional[str] = Field(None, max_length=500)
    is_renewed: Optional[bool] = None


class ProductResponse(ProductBase):
    id: UUID
    contract_start_date: datetime
    contract_end_date: datetime
    is_renewed: bool
    status: ProductStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    total: int
    page: int
    per_page: int
    products: list[ProductResponse]


class DashboardStats(BaseModel):
    total_products: int
    active_products: int
    expired_products: int
    expiring_soon_7_days: int
    expiring_soon_30_days: int
