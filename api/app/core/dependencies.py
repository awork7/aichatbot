from fastapi import HTTPException
from typing import Optional
from app.services.rag_service import RAGService
from app.utils.cache import CacheManager

# Global instances (will be set during startup)
_rag_service: Optional[RAGService] = None
_cache_manager: Optional[CacheManager] = None

def set_rag_service(rag_service: RAGService):
    """Set the global RAG service instance"""
    global _rag_service
    _rag_service = rag_service

def set_cache_manager(cache_manager: CacheManager):
    """Set the global cache manager instance"""
    global _cache_manager
    _cache_manager = cache_manager

def get_rag_service() -> RAGService:
    """Dependency to get RAG service"""
    if not _rag_service or not _rag_service.is_ready:
        raise HTTPException(status_code=503, detail="RAG service not available")
    return _rag_service

def get_cache_manager() -> CacheManager:
    """Dependency to get cache manager"""
    if not _cache_manager:
        raise HTTPException(status_code=503, detail="Cache service not available")
    return _cache_manager
