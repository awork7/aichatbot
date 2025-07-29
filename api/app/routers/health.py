from fastapi import APIRouter, Depends
from app.models.response import HealthResponse
from app.services.rag_service import RAGService
from app.utils.cache import CacheManager
from app.core.config import get_settings
from app.core.dependencies import get_rag_service, get_cache_manager  # Fixed import
import psutil
import time

router = APIRouter()

@router.get("/", response_model=HealthResponse)
async def health_check():
    """Basic health check"""
    return HealthResponse(
        status="healthy",
        components={"api": "healthy"},
        version=get_settings().VERSION
    )

@router.get("/detailed", response_model=HealthResponse)
async def detailed_health_check(
    rag_service: RAGService = Depends(get_rag_service),
    cache_manager: CacheManager = Depends(get_cache_manager)
):
    """Detailed health check with all components"""
    try:
        # Get RAG service health
        rag_health = await rag_service.get_health_status()
        
        # Get cache health
        cache_health = await cache_manager.health_check()
        
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        components = {
            "rag_service": rag_health["status"],
            "cache": "healthy" if cache_health else "unhealthy",
            "system": {
                "cpu_usage": f"{cpu_percent}%",
                "memory_usage": f"{memory.percent}%",
                "disk_usage": f"{(disk.used / disk.total) * 100:.1f}%"
            },
            "llm": rag_health["components"]["llm"],
            "documents": rag_health["components"]["documents"]
        }
        
        overall_status = "healthy" if all(
            status == "healthy" for status in [
                rag_health["status"],
                "healthy" if cache_health else "unhealthy"
            ]
        ) else "unhealthy"
        
        return HealthResponse(
            status=overall_status,
            components=components,
            version=get_settings().VERSION
        )
        
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            components={"error": str(e)},
            version=get_settings().VERSION
        )

@router.get("/ready")
async def readiness_check(rag_service: RAGService = Depends(get_rag_service)):
    """Kubernetes readiness probe"""
    if rag_service.is_ready:
        return {"status": "ready"}
    else:
        return {"status": "not_ready"}, 503

@router.get("/live")
async def liveness_check():
    """Kubernetes liveness probe"""
    return {"status": "alive", "timestamp": time.time()}
