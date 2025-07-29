from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.security import HTTPBearer
from typing import Dict, Any, Optional
import time
import uuid
from datetime import datetime

from app.models.request import ChatRequest
from app.models.response import ChatResponse, ErrorResponse
from app.services.rag_service import RAGService
from app.utils.cache import CacheManager
from app.utils.monitoring import REQUEST_COUNT, ACTIVE_SESSIONS
from app.core.logging import get_logger
from app.main import get_rag_service, get_cache_manager

router = APIRouter()
logger = get_logger(__name__)
security = HTTPBearer(auto_error=False)

@router.post("/message", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    rag_service: RAGService = Depends(get_rag_service),
    cache_manager: CacheManager = Depends(get_cache_manager)
):
    """Send a message to the chatbot"""
    session_id = request.session_id or str(uuid.uuid4())
    
    try:
        # Increment active sessions
        ACTIVE_SESSIONS.inc()
        
        # Validate message length
        if len(request.message) > 1000:
            raise HTTPException(status_code=400, detail="Message too long")
        
        # Rate limiting check (implement based on session_id)
        # await check_rate_limit(session_id, cache_manager)
        
        # Process the query
        start_time = time.time()
        result = await rag_service.query(request.message, session_id)
        
        # Create response
        response = ChatResponse(
            answer=result["answer"],
            sources=result.get("sources", []),
            response_time=result["response_time"],
            session_id=session_id,
            timestamp=datetime.utcnow()
        )
        
        # Log successful request
        REQUEST_COUNT.labels(method="POST", endpoint="chat", status="success").inc()
        
        # Background task to cache conversation
        background_tasks.add_task(
            cache_conversation,
            cache_manager,
            session_id,
            request.message,
            result["answer"]
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat error: {e}", extra={"session_id": session_id})
        REQUEST_COUNT.labels(method="POST", endpoint="chat", status="error").inc()
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        ACTIVE_SESSIONS.dec()

@router.get("/history/{session_id}")
async def get_chat_history(
    session_id: str,
    limit: int = 50,
    cache_manager: CacheManager = Depends(get_cache_manager)
):
    """Get chat history for a session"""
    try:
        history = await cache_manager.get_chat_history(session_id, limit)
        return {"session_id": session_id, "history": history}
    except Exception as e:
        logger.error(f"Error retrieving chat history: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve chat history")

@router.delete("/history/{session_id}")
async def clear_chat_history(
    session_id: str,
    cache_manager: CacheManager = Depends(get_cache_manager)
):
    """Clear chat history for a session"""
    try:
        await cache_manager.clear_chat_history(session_id)
        return {"message": "Chat history cleared", "session_id": session_id}
    except Exception as e:
        logger.error(f"Error clearing chat history: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear chat history")

async def cache_conversation(
    cache_manager: CacheManager,
    session_id: str,
    user_message: str,
    assistant_response: str
):
    """Background task to cache conversation"""
    try:
        await cache_manager.add_to_chat_history(
            session_id,
            user_message,
            assistant_response
        )
    except Exception as e:
        logger.error(f"Failed to cache conversation: {e}")
