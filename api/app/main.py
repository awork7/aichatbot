from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
import logging
from typing import Dict, Any

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.routers import chat, health, services, admin
from app.services.rag_service import RAGService
from app.utils.monitoring import REQUEST_COUNT, setup_metrics
from app.utils.cache import CacheManager

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Global instances
rag_service: RAGService = None
cache_manager: CacheManager = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    global rag_service, cache_manager
    
    settings = get_settings()
    logger.info("Starting SIB AI Chatbot API...")
    
    try:
        # Initialize cache
        cache_manager = CacheManager(settings.REDIS_URL)
        await cache_manager.initialize()
        
        # Initialize RAG service
        rag_service = RAGService(settings)
        await rag_service.initialize()
        
        # Setup monitoring
        setup_metrics()
        
        app.state.rag_service = rag_service
        app.state.cache_manager = cache_manager
        
        logger.info("✅ All services initialized successfully")
        
        yield
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize services: {e}")
        raise
    finally:
        # Cleanup
        if rag_service:
            await rag_service.cleanup()
        if cache_manager:
            await cache_manager.close()
        logger.info("Application shutdown complete")

# Create FastAPI app
settings = get_settings()
app = FastAPI(
    title="SIB AI Chatbot API",
    description="Production-ready South Indian Bank AI Assistant",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(services.router, prefix="/api/v1/services", tags=["services"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "SIB AI Chatbot API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs" if settings.ENVIRONMENT == "development" else "disabled"
    }

# Serve static files (React build) in production
if settings.ENVIRONMENT == "production":
    app.mount("/", StaticFiles(directory="frontend/build", html=True), name="static")

def get_rag_service() -> RAGService:
    """Dependency to get RAG service"""
    if not rag_service or not rag_service.is_ready:
        raise HTTPException(status_code=503, detail="RAG service not available")
    return rag_service

def get_cache_manager() -> CacheManager:
    """Dependency to get cache manager"""
    if not cache_manager:
        raise HTTPException(status_code=503, detail="Cache service not available")
    return cache_manager

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower()
    )
