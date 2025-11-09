from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timedelta
import uuid
import enum
from app.models.base import Base


class ProductStatus(str, enum.Enum):
    ACTIVE = "Active"
    EXPIRED = "Expired"
    EXPIRING_SOON = "ExpiringSoon"


class Product(Base):
    __tablename__ = "products"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    bot_username = Column(String(255))
    website_link = Column(String(500))
    contract_months = Column(Integer, nullable=False)  # 1-12 months
    contract_start_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    contract_end_date = Column(DateTime, nullable=False)
    is_renewed = Column(Boolean, default=False)
    status = Column(SQLEnum(ProductStatus), nullable=False, default=ProductStatus.ACTIVE, index=True)
    customer_telegram = Column(String(255), index=True)
    customer_link = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.contract_start_date and self.contract_months and not self.contract_end_date:
            self.contract_end_date = self.contract_start_date + timedelta(days=30 * self.contract_months)
        self.update_status()
    
    def update_status(self):
        """Update product status based on contract dates."""
        if not self.contract_end_date:
            return
        
        now = datetime.utcnow()
        days_until_expiry = (self.contract_end_date - now).days
        
        if days_until_expiry < 0:
            self.status = ProductStatus.EXPIRED
        elif days_until_expiry <= 7:
            self.status = ProductStatus.EXPIRING_SOON
        else:
            self.status = ProductStatus.ACTIVE
