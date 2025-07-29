from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import logging

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.core.dependencies import set_rag_service, set_cache_manager
from app.routers import chat, health, services, admin
from app.services.rag_service import RAGService
from app.utils.monitoring import setup_metrics
from app.utils.cache import CacheManager

# Setup logging FIRST
setup_logging()
logger = logging.getLogger(__name__)  # Add this line!

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    settings = get_settings()
    logger.info("Starting SIB AI Chatbot API...")  # Now logger is defined
    
    try:
        cache_manager = CacheManager(settings.REDIS_URL)
        await cache_manager.initialize()
        
        rag_service = RAGService(settings)
        await rag_service.initialize()
        
        setup_metrics()
        
        set_rag_service(rag_service)
        set_cache_manager(cache_manager)
        
        logger.info("✅ All services initialized successfully")
        yield
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize services: {e}")
        raise
    finally:
        logger.info("Application shutdown complete")

# Rest of your FastAPI app configuration...
settings = get_settings()
app = FastAPI(
    title="SIB AI Chatbot API",
    description="Production-ready South Indian Bank AI Assistant",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000", 
        "http://localhost:3001",
        "http://127.0.0.1:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(services.router, prefix="/api/v1/services", tags=["services"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])

@app.get("/")
async def root():
    return {
        "message": "SIB AI Chatbot API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs" if settings.ENVIRONMENT == "development" else "disabled"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower()
    )
