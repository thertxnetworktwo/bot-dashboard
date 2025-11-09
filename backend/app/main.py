from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
from app.core.config import settings
from app.core.database import engine
from app.models.base import Base
from app.api.routes import health, products, phone_registry

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info("Starting Telegram Bot Dashboard API...")
    
    # Create tables if they don't exist (for development)
    if settings.ENV == "development":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created/verified")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Telegram Bot Dashboard API...")
    await engine.dispose()


# Create FastAPI app
app = FastAPI(
    title="Telegram Bot Dashboard API",
    description="API for managing Telegram bot products with phone registry integration",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
# Parse CORS origins from comma-separated string
cors_origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(products.router)
app.include_router(phone_registry.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.ENV == "development"
    )
