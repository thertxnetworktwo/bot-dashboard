from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID
from app.api.deps import get_db
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse,
    DashboardStats,
    ProductStatus
)
from app.services.product_service import ProductService

router = APIRouter(prefix="/api/products", tags=["products"])


@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new product."""
    product = await ProductService.create_product(db, product_data)
    return product


@router.get("/", response_model=ProductListResponse)
async def list_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    status: Optional[ProductStatus] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get paginated list of products."""
    skip = (page - 1) * per_page
    products, total = await ProductService.get_products(
        db, skip=skip, limit=per_page, status=status, search=search
    )
    
    return ProductListResponse(
        total=total,
        page=page,
        per_page=per_page,
        products=products
    )


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    """Get dashboard statistics."""
    stats = await ProductService.get_dashboard_stats(db)
    return stats


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific product by ID."""
    product = await ProductService.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: UUID,
    product_data: ProductUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a product."""
    product = await ProductService.update_product(db, product_id, product_data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Delete a product."""
    success = await ProductService.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return None


@router.post("/{product_id}/renew", response_model=ProductResponse)
async def renew_product(
    product_id: UUID,
    months: int = Query(..., ge=1, le=12),
    db: AsyncSession = Depends(get_db)
):
    """Renew a product by extending the contract."""
    product = await ProductService.renew_product(db, product_id, months)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
