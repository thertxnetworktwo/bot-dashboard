from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from typing import Optional, List
from datetime import datetime, timedelta
from uuid import UUID
from app.models.product import Product, ProductStatus
from app.schemas.product import ProductCreate, ProductUpdate, DashboardStats


class ProductService:
    @staticmethod
    async def create_product(db: AsyncSession, product_data: ProductCreate) -> Product:
        """Create a new product."""
        product = Product(**product_data.model_dump())
        db.add(product)
        await db.flush()
        await db.refresh(product)
        return product
    
    @staticmethod
    async def get_product(db: AsyncSession, product_id: UUID) -> Optional[Product]:
        """Get a product by ID."""
        result = await db.execute(select(Product).where(Product.id == product_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_products(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 50,
        status: Optional[ProductStatus] = None,
        search: Optional[str] = None
    ) -> tuple[List[Product], int]:
        """Get paginated list of products with optional filters."""
        query = select(Product)
        count_query = select(func.count(Product.id))
        
        # Apply filters
        if status:
            query = query.where(Product.status == status)
            count_query = count_query.where(Product.status == status)
        
        if search:
            search_filter = (
                Product.name.ilike(f"%{search}%") |
                Product.description.ilike(f"%{search}%") |
                Product.customer_telegram.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)
        
        # Get total count
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Get paginated results
        query = query.order_by(Product.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        products = result.scalars().all()
        
        return list(products), total
    
    @staticmethod
    async def update_product(
        db: AsyncSession,
        product_id: UUID,
        product_data: ProductUpdate
    ) -> Optional[Product]:
        """Update a product."""
        product = await ProductService.get_product(db, product_id)
        if not product:
            return None
        
        update_data = product_data.model_dump(exclude_unset=True)
        
        # If contract_months is updated, recalculate end date
        if 'contract_months' in update_data:
            product.contract_months = update_data['contract_months']
            product.contract_end_date = product.contract_start_date + timedelta(
                days=30 * product.contract_months
            )
        
        # Update other fields
        for field, value in update_data.items():
            if field != 'contract_months':
                setattr(product, field, value)
        
        # Update status based on new dates
        product.update_status()
        product.updated_at = datetime.utcnow()
        
        await db.flush()
        await db.refresh(product)
        return product
    
    @staticmethod
    async def delete_product(db: AsyncSession, product_id: UUID) -> bool:
        """Delete a product."""
        product = await ProductService.get_product(db, product_id)
        if not product:
            return False
        
        await db.delete(product)
        await db.flush()
        return True
    
    @staticmethod
    async def renew_product(db: AsyncSession, product_id: UUID, months: int) -> Optional[Product]:
        """Renew a product by extending contract."""
        product = await ProductService.get_product(db, product_id)
        if not product:
            return None
        
        # Extend from current end date or now, whichever is later
        base_date = max(product.contract_end_date, datetime.utcnow())
        product.contract_end_date = base_date + timedelta(days=30 * months)
        product.is_renewed = True
        product.update_status()
        product.updated_at = datetime.utcnow()
        
        await db.flush()
        await db.refresh(product)
        return product
    
    @staticmethod
    async def get_dashboard_stats(db: AsyncSession) -> DashboardStats:
        """Get dashboard statistics."""
        # Total products
        total_result = await db.execute(select(func.count(Product.id)))
        total = total_result.scalar()
        
        # Active products
        active_result = await db.execute(
            select(func.count(Product.id)).where(Product.status == ProductStatus.ACTIVE)
        )
        active = active_result.scalar()
        
        # Expired products
        expired_result = await db.execute(
            select(func.count(Product.id)).where(Product.status == ProductStatus.EXPIRED)
        )
        expired = expired_result.scalar()
        
        # Expiring in 7 days
        now = datetime.utcnow()
        seven_days = now + timedelta(days=7)
        expiring_7_result = await db.execute(
            select(func.count(Product.id)).where(
                and_(
                    Product.contract_end_date <= seven_days,
                    Product.contract_end_date > now
                )
            )
        )
        expiring_7 = expiring_7_result.scalar()
        
        # Expiring in 30 days
        thirty_days = now + timedelta(days=30)
        expiring_30_result = await db.execute(
            select(func.count(Product.id)).where(
                and_(
                    Product.contract_end_date <= thirty_days,
                    Product.contract_end_date > now
                )
            )
        )
        expiring_30 = expiring_30_result.scalar()
        
        return DashboardStats(
            total_products=total,
            active_products=active,
            expired_products=expired,
            expiring_soon_7_days=expiring_7,
            expiring_soon_30_days=expiring_30
        )
