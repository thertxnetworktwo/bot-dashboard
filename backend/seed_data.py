"""
Seed script to populate database with sample product data
Run with: python seed_data.py
"""
import asyncio
import sys
import os
from datetime import datetime, timedelta
from uuid import uuid4

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.database import AsyncSessionLocal
from app.models.product import Product, ProductStatus


async def seed_products():
    """Create sample products for testing."""
    
    sample_products = [
        {
            "name": "Premium Bot",
            "description": "Advanced Telegram bot with AI capabilities",
            "bot_username": "premium_ai_bot",
            "contract_months": 12,
            "contract_start_date": datetime.utcnow() - timedelta(days=30),
            "customer_telegram": "@john_doe",
        },
        {
            "name": "Marketing Bot",
            "description": "Automated marketing and promotion bot",
            "bot_username": "marketing_pro_bot",
            "contract_months": 6,
            "contract_start_date": datetime.utcnow() - timedelta(days=150),
            "customer_telegram": "@jane_smith",
        },
        {
            "name": "Support Bot",
            "description": "24/7 customer support automation",
            "website_link": "https://support-bot.example.com",
            "contract_months": 3,
            "contract_start_date": datetime.utcnow() - timedelta(days=85),
            "customer_telegram": "@support_team",
        },
        {
            "name": "Analytics Bot",
            "description": "Data analytics and reporting bot",
            "bot_username": "analytics_bot",
            "contract_months": 12,
            "contract_start_date": datetime.utcnow() - timedelta(days=10),
            "customer_telegram": "@data_team",
        },
        {
            "name": "Notification Bot",
            "description": "Smart notification delivery system",
            "bot_username": "notify_bot",
            "contract_months": 1,
            "contract_start_date": datetime.utcnow() - timedelta(days=25),
            "customer_telegram": "@notify_admin",
        },
    ]
    
    async with AsyncSessionLocal() as session:
        print("Creating sample products...")
        
        for product_data in sample_products:
            product = Product(**product_data)
            session.add(product)
            print(f"  ✓ Created: {product.name} (Status: {product.status})")
        
        await session.commit()
        print(f"\n✅ Successfully created {len(sample_products)} sample products!")


async def clear_products():
    """Clear all products from database."""
    async with AsyncSessionLocal() as session:
        result = await session.execute("DELETE FROM products")
        await session.commit()
        print("✅ All products cleared!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Seed database with sample data")
    parser.add_argument("--clear", action="store_true", help="Clear all products first")
    args = parser.parse_args()
    
    if args.clear:
        print("Clearing existing products...")
        asyncio.run(clear_products())
    
    asyncio.run(seed_products())
