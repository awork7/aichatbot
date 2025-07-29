from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.request import AdminRequest
from app.services.rag_service import RAGService
from app.core.config import get_settings
from app.core.dependencies import get_rag_service  # Fixed import
import logging

router = APIRouter()
security = HTTPBearer()
logger = logging.getLogger(__name__)

def verify_admin_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify admin authentication token"""
    settings = get_settings()
    if credentials.credentials != settings.SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid admin token")
    return credentials

@router.post("/reload-documents")
async def reload_documents(
    rag_service: RAGService = Depends(get_rag_service),
    credentials: HTTPAuthorizationCredentials = Depends(verify_admin_token)
):
    """Reload documents from data directory"""
    try:
        await rag_service._load_documents()
        return {"message": "Documents reloaded successfully", "count": len(rag_service.sib_content)}
    except Exception as e:
        logger.error(f"Failed to reload documents: {e}")
        raise HTTPException(status_code=500, detail="Failed to reload documents")

@router.get("/system-info")
async def get_system_info(
    rag_service: RAGService = Depends(get_rag_service),
    credentials: HTTPAuthorizationCredentials = Depends(verify_admin_token)
):
    """Get detailed system information"""
    import psutil
    
    return {
        "system": {
            "cpu_count": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total,
            "disk_total": psutil.disk_usage('/').total
        },
        "rag_service": {
            "is_ready": rag_service.is_ready,
            "documents_loaded": len(rag_service.sib_content),
            "model": rag_service.settings.MODEL_NAME
        },
        "settings": {
            "environment": get_settings().ENVIRONMENT,
            "version": get_settings().VERSION
        }
    }
