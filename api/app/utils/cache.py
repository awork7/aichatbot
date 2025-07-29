import redis.asyncio as redis
import json
import logging
from typing import Any, Optional, List, Dict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis_client: Optional[redis.Redis] = None
    
    async def initialize(self):
        """Initialize Redis connection"""
        try:
            self.redis_client = redis.from_url(self.redis_url)
            await self.redis_client.ping()
            logger.info("✅ Cache manager initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize cache: {e}")
            raise
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            if not self.redis_client:
                return None
            
            value = await self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: int = 3600):
        """Set value in cache with TTL"""
        try:
            if not self.redis_client:
                return False
            
            serialized_value = json.dumps(value, default=str)
            await self.redis_client.setex(key, ttl, serialized_value)
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    async def delete(self, key: str):
        """Delete key from cache"""
        try:
            if self.redis_client:
                return await self.redis_client.delete(key)
            return False
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False
    
    async def add_to_chat_history(self, session_id: str, user_message: str, assistant_response: str):
        """Add conversation to chat history"""
        try:
            key = f"chat_history:{session_id}"
            conversation = {
                "user_message": user_message,
                "assistant_response": assistant_response,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            await self.redis_client.lpush(key, json.dumps(conversation))
            await self.redis_client.ltrim(key, 0, 49)  # Keep last 50 messages
            await self.redis_client.expire(key, 86400)  # 24 hours
            
        except Exception as e:
            logger.error(f"Failed to add to chat history: {e}")
    
    async def get_chat_history(self, session_id: str, limit: int = 50) -> List[Dict]:
        """Get chat history for session"""
        try:
            key = f"chat_history:{session_id}"
            messages = await self.redis_client.lrange(key, 0, limit - 1)
            
            history = []
            for msg in messages:
                try:
                    history.append(json.loads(msg))
                except json.JSONDecodeError:
                    continue
            
            return list(reversed(history))  # Return in chronological order
            
        except Exception as e:
            logger.error(f"Failed to get chat history: {e}")
            return []
    
    async def clear_chat_history(self, session_id: str):
        """Clear chat history for session"""
        try:
            key = f"chat_history:{session_id}"
            await self.redis_client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Failed to clear chat history: {e}")
            return False
    
    async def health_check(self) -> bool:
        """Check cache health"""
        try:
            if not self.redis_client:
                return False
            await self.redis_client.ping()
            return True
        except Exception:
            return False
    
    async def close(self):
        """Close Redis connection"""
        if self.redis_client:
            await self.redis_client.close()

def cache_result(ttl: int = 3600):
    """Decorator for caching function results"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Simple cache key generation
            cache_key = f"func_cache:{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache first
            # Implementation would depend on having access to cache manager
            
            # If not in cache, execute function and cache result
            result = await func(*args, **kwargs)
            return result
        
        return wrapper
    return decorator
